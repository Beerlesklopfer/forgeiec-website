---
title: "Security architecture in 3 layers"
date: 2026-05-08
summary: "Per-variable force gate, Confirmation State Machine, build-time gating — how ForgeIEC prevents an AI or a misclick from moving real hardware"
components: [studio, anvild]
---

{{< components "studio,anvild" >}}

## What it's about

In automation the most dangerous command is **force**: manually
pinning an output pin to TRUE, independent of the program. This
moves **real hardware** at the output — a motor, a valve, a
safety function.

ForgeIEC treats force settings accordingly: **per-variable gated,
with three sequential defence layers** in independent subsystems.
An AI **cannot** force. A misclick in the UI requires two
separate confirmations. And a production runtime build does not
even include the force bridge.

---

## Layer 1 — codegen TOML

Already at compile time the editor decides per variable whether
`force_enabled` is written into `bellows_descriptor.toml`. Variables
without the flag do **not** land in the force bridge:

- The Variables tab has an `F` checkbox per variable
- Default: OFF (force not allowed)
- Turning it on is a model change that makes the project dirty →
  must be saved + re-deployed

This anchors force authorisation at **source code level**.
Operator + audit can see exactly which variables are forceable.

---

## Layer 2 — anvild RPC

The anvild runtime checks the build mode of the running PLC
binary at the `ForceVariable` gRPC endpoint. If the binary was
**not** built with the force bridge, anvild refuses force requests
— regardless of what the UI says.

Production runtime builds ship without `-DFORCING_ENABLED`. Even
if an attacker compromises Studio, they cannot force a setting on
the real PLC because the code path doesn't exist there.

---

## Layer 3 — editor UI

The F checkbox is **automatically greyed out** when the PLC binary
does not support force. Plus: build mode info flows through
`anvild::server_info` to the editor —
`editor_build.force_available` is `true|false`.

Operator sees in the UI immediately: this is a safe production
binary, force is not possible. No "click and hope" trial and error.

---

## Layer 4 — MCP

For the **AI layer** there is a fourth layer on top: there is **no**
`force.*` MCP tool, neither in default nor override build. An AI
can **read** the `forced=true|false` state (via `monitor.snapshot`),
but **cannot set** it.

Rationale in the spec (mcp-platform-v1 §7.4): "An AI agent must
not trigger such side effects on its own — even if it thinks it
is right."

---

## Plus: Confirmation State Machine for all changes

Force is only the strictest variant. In general **every write
action** by the AI goes through a state machine:

1. Tool call returns `FORGE_ERR_CONFIRMATION_REQUIRED`
2. Operator sees in the chat: what is about to happen + context
3. Confirmation via `editor.confirm` resumes the tool
4. Audit log with timestamp, tool, args, choice

```
Confirmation required:
  Tool: project.write.add_variable
  Question: Add bellows.Bellows.LED_00 (iec_type=BOOL)?
  Options: yes / cancel
```

Even fast mode (auto-confirm) must be deliberately turned on —
with an extra safety warning. In production: leave it off. Plus
the emergency stop as a red industrial mushroom button.

---

## What the commits delivered

- `9cc6dcd` — per-variable force gate, 3-layer defence complete
- `dbfd62a` — Confirmation State Machine (FConfirmationStateMachine)
  + project.* lifecycle + audit log
- `4ce57bf` — codegen.deploy gate requires
  `MCP_OVERRIDE_SECURITIES`, no runtime switch
- `f43c9d7` — industrial E-stop + danger mode settings with
  explicit warning
- `0699954` — danger mode auto-confirm + per-settings tool-loop
  limit
- `b489428` — anvild build-info propagation via `server_info` ⇒
  editor-side force-greyout logic

Plus architecture spec: `documentation/architecture/mcp-platform-v1.md`
§9 (security model) + tongs-platform-v1 §5 (fault model for bus
bridges).

---

## Where you use it

| You want | Configuration |
|---|---|
| Production PLC, AI read-only | Standard APT install, no override flag |
| Development with force testing | Mark force vars one by one, dev runtime build |
| Repair workshop: lifecycle automatable | Danger mode per persona — see [daily operation](/help/ai/chat/) |
| Test loop without UI click for 50 variables | Danger mode + raised tool-turn limit |
| Onboarding | Trainee persona, always all confirms |

---

## Where to read more

- [Security model (user)](/help/ai/security/)
- [Architecture + Security (auditor)](/help/ai/architecture/)
- [Personas — who may do what](/help/ai/agents/)
