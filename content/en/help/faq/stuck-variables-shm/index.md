---
title: "Variable 'sticks' despite a fresh deploy"
summary: "BOOL/INT value holds against the program logic — usually caused by stale Anvil shared memory"
---

{{< callout type="symptom" title="Symptom" >}}
A BOOL or INT pool variable holds a value (TRUE/FALSE or numeric)
that doesn't match the program logic. `monitor.snapshot` reports
`forced=false`, the ST code clearly writes a different value — and
still the value stays "glued". **Cause: stale Anvil shared
memory.**
{{< /callout >}}

Classic picture:

- The Variables tab shows `TRUE` as the value
- The F checkbox is **not** set (`forced = false`)
- The ST code clearly writes a different value
  (e.g. `Bellows.LED_14 := (Position = 14);` and Position is never 14)
- A fresh compile + deploy report "Compilation finished successfully" —
  but the behaviour does not change

You restart ForgeIEC Studio, anvild, bellowsd — and the value stays.

---

## Cause

ForgeIEC uses the **Anvil** zero-copy shared-memory layer for data
transport between the PLC runtime, the editor, and the HMI bridges.
The shared-memory segments and the shared service registry are kept
as files under `/dev/shm/` and below `/tmp/`.

When a PLC process is killed hard (e.g. crashed deploy, SIGKILL while
publishes are in flight, watchdog reset), a **subscriber queue with a
stale payload** can remain in the file.

On the next start, `bellows_subscribe_all()` polls exactly this queue
— and writes the old TRUE values back into PLC memory **before** the
POU is allowed to run.

Because this happens before every scan cycle, the old value gets
"latched", even when the POU computes something else in the same
cycle — at the next cycle the stale payload arrives again.

A typical sign is that only **individual bits** are affected (exactly
those whose stale payload still lives in SHM); other variables on the
same topic cycle normally.

---

{{< callout type="solution" title="Solution — restart the PLC runtime" >}}
Anvil reclaims the segments of **crashed peers** by itself: every
time a new Anvil node is created, the resources of dead nodes are
reaped — without touching live peers. So restarting the PLC runtime
is enough:

In ForgeIEC Studio use `Stop` + `Start` from the runtime menu, or
`Build → Compile and Upload` directly. The SHM topics are created
fresh, without a stale payload.
{{< /callout >}}

After the next scan cycle, the live monitor shows the correct value
computed by your program logic.

{{< callout type="warning" title="Do not delete SHM files by hand" >}}
Older guides recommended an `rm -rf` on the SHM files as an
emergency fix. **Do not do this while the system is running.** The
segments and the service registry are the **shared store of all
Anvil peers** — anvild, bellowsd, hearth and the tongs bridges all
depend on them. A blanket wipe rips the segments away from live
peers; the Anvil bus then falls apart **silently**, with no retry
and no self-healing.

For exactly that reason anvild no longer wipes on startup or on PLC
stop — the Anvil layer does the cleanup selectively, per dead node.

If something does stay stuck: stop all Anvil peers together
(`bellowsd`, `hearth`, `tongs-*`, `anvild`) and start them again.
With no live nodes around, the segments of dead nodes are reclaimed
cleanly.
{{< /callout >}}

---

## When does this happen?

In a normal devloop **this practically never happens**. A clean deploy
via `Build -> Compile and Upload` and proper stop+start through the
Runtime menu cleans the SHM topics on the regular path.

The effect mainly shows up in one scenario:

**You let the local AI assistant (MCP) experiment on the project.**
The LLM may have:

- Repeatedly run `set_text_body` + `codegen.deploy` in quick succession
- Forced variables and not released them cleanly
- Renamed or deleted POU instances while the PLC was still running
- Tried several deploy iterations without `runtime.stop` in between

Such sequences can create a brief moment in which the old forgeiec-plc
instance is terminated with `SIGTERM`/`SIGKILL` before it can withdraw
its subscriber queues from the SHM — and exactly that queue is then
read back in by the NEW forgeiec-plc instance at startup.

Rarer triggers without AI involvement:

- Hard `kill -9` on `forgeiec-plc` by the operator
- Crashes of the HMI bridge (`bellowsd`) during operation
- Mixed operation of different anvild versions on the same host

If it happens once, the runtime restart above is the simplest fix.
For repeated occurrences without AI activity, please report the
incident (with `journalctl -u anvild` and `journalctl -u bellowsd`
from the last hour) to blacksmith@forgeiec.io — targeted, selective
reaping of dead nodes from within Studio is an ongoing backlog item.

---

## Related

- [Online Help](/help/online/) — context-sensitive editor help
- [Test Coverage](/help/tests/) — automated test suite
