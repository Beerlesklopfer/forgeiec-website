---
title: "Security model"
summary: "How ForgeIEC prevents the AI from accidentally causing damage — three protection layers"
---

## The basic principle

An AI in an industrial editor is dangerous if it can switch
unsupervised. A **forced output** could start a motor. A **wrong
deploy** could stop a running plant. An **accidentally deleted
variable** could disable a safety function.

ForgeIEC's answer: **three sequential protection layers**. An AI
must pass all three before it can change anything in your plant.

---

## Layer 1 — The default install is safe

When you install ForgeIEC fresh from the APT repository, the AI
assistant is in **read-only mode**. It can:

- Read (project, POUs, live values)
- Suggest things ("there's a bug here")
- Produce diagnostic reports

It **cannot**:

- Create or delete variables
- Modify POU code
- Compile or deploy
- Start / stop / pause the PLC

This is not a checkbox you flip — it is a **different editor
version**. The default version from the internet **simply does
not include** the write functions.

To allow write actions, the editor must be freshly built with the
option `-DMCP_OVERRIDE_SECURITIES=ON` — or you install the bundled
dev package. **On a productive PLC workstation, that should not
run.**

You can recognise it: when the editor is started with write
permission, the AI assistant shows a **security banner** at
startup:

```
!!! SECURITY OVERRIDE ACTIVE !!!
Editor was built with MCP_OVERRIDE_SECURITIES=ON
ALL MCP security gates are OPEN
This build MUST NOT run on a productive PLC.
```

---

## Layer 2 — A question for every change

Even in the unlocked version, the editor asks a question for
**every** writing action.

Example: the AI wants to create a variable.

```
[tool] project.write.add_variable
        name=Pressure_1, iec_type=REAL, address=%MD200, scope=bellows.Sensors

Confirmation required:
  Question: Add bellows.Sensors.Pressure_1 (iec_type=REAL)?
  Options:  yes / cancel
```

Only when you click **"yes"** does the action happen. If you click
**"cancel"**, the AI loop breaks cleanly and the AI is told you
refused — it can then go a different way or ask.

These questions appear **visibly in the chat log** — the AI
assistant cannot bypass you "in secret".

**In Fast mode** (see [Daily operation](/help/ai/chat/)) the editor
answers these questions **itself with "yes"**. Convenient for test
setups but **not recommended for production** — applies only to
the current request and must be deliberately turned on.

---

## Layer 3 — Operator visibility

The AI cannot do anything **silently**. Everything is readable:

- **In the chat log** you see every AI tool call:
  `[tool] codegen.deploy (0 args)`
- **In the output panel** you see the compile output as if you had
  pressed the build button yourself.
- **In the audit log** every write action is recorded with a
  timestamp. The file lives at `~/.config/ForgeIEC/mcp_audit.log`
  and can be reviewed later.

---

## Force path — the red line

One action is **on principle** not accessible to the AI:
**forcing**. "Forcing" means manually pinning a variable's value
regardless of what the program says — e.g. setting an output pin
to TRUE, which can start a motor on the hardware.

Force settings must be made by the **human via the GUI**. The AI
can see them (in the live snapshot they show `forced=true`) but
**cannot set them**. This is a **hard separation** — independent
of Fast mode, independent of the build flag.

Rationale: a forced output moves **real hardware**. Safety and
protection functions could be overridden by it. An AI agent must
not trigger such side effects on its own — even if it thinks it
is right.

---

## What to do when something goes wrong

1. **Emergency stop** (red STOP button in the AI panel, visible
   only in Fast mode) → break the AI loop immediately
2. **Stop the PLC** via the `Runtime` menu → outputs to safe state
3. **Release forced variables** via the Force tab in the
   Variables panel
4. **Read the audit log** at `~/.config/ForgeIEC/mcp_audit.log`
   → what the AI did in sequence

---

## Recommendations

- **Development:** unlocked version, Trainee persona, slow mode —
  you see every step
- **Code review:** Reviewer persona — cannot break anything
- **Diagnosis on a production PLC:** Monitor persona — no changes
  possible
- **Active programming with experienced AI:** Blacksmith Master,
  possibly Fast mode on
- **Productive operation on a running plant:** keep the default
  version installed — AI is read-only, no danger

---

## Next

- [Daily operation](/help/ai/chat/) — emergency stop + Fast mode
- [Personas](/help/ai/agents/) — which characters have which
  rights
- [Connecting multiple workstations](/help/ai/team/) — team trust
- [Back to the AI overview](/help/ai/)
