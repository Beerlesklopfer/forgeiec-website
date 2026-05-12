---
title: "The AI assistant in the editor: from chat to platform"
date: 2026-05-12
summary: "Built-in AI assistant with ~80 tools, multi-persona workflow, open connector for Claude Desktop, VS Code, ChatGPT"
components: [studio, anvild]
---

{{< components "studio,anvild" >}}

## Why this matters

AI code assistance is well established in the software world — not
so in industrial automation. Reason: PLC code drives real hardware,
every wrong variable moves a motor or opens a valve. Cloud LLMs as
"code completion for PLCs" do not work without a strict security
layer.

ForgeIEC Studio solves this with **MCP (Model Context Protocol)** as
the interface between LLM and editor. The LLM calls typed tools —
no free-form shell commands — and every change-causing step goes
through operator confirmation.

That makes ForgeIEC the first IEC 61131-3 editor with **seriously
viable** AI integration.

---

## What the AI does in practice

Six tool families cover the editor surface:

| Family | What the AI sees / does |
|---|---|
| `project.*` | POU inventory, create variables, write POU bodies, inspect bus topology |
| `codegen.*` | Compile, generate, deploy, status polling with g++ stderr tail |
| `monitor.*` | Live snapshot + single values + cycle stats + code state |
| `oscilloscope.*` | Time-series capture with trigger, stream API, CSV export |
| `tasks.*` | Read + write resource/task/program instance |
| `library.*` | Standard FB blocks (TON, CTU, R_TRIG, …) lookup with ST examples |
| `bellows.*`, `anvil.*` | HMI gateway + Anvil topic inspection |
| `editor.*` | Clean quit, logs, confirm responses |
| `forge.help` | Self-doc — the AI queries itself |

Over **80 tools** in total, all JSON-Schema-typed and
self-describing via `forge.help_for(name)` with examples + error
classes.

---

## Five personas, one chat tab

Instead of a single static session, **role-based personas** in the
AI tab:

- **Blacksmith Master** — the foreman, may do everything
- **Reviewer** — read-only, cannot break anything
- **Doc** — writes variable comments + docs
- **Monitor** — watches live plants, no changes
- **Trainee** — like the foreman, but every action confirmed
  individually — ideal for onboarding

Every persona has **its own API endpoint + model** — so GPT-4o can
write the code and Claude Opus reviews it.

More: [Personas in detail](/help/ai/agents/).

---

## Open — no vendor lock-in

The editor implements the **server side** of MCP. Any MCP-compliant
client can connect — the built-in chat tab is only one of them:

- **Claude Desktop** (Mac, Windows, Linux)
- **VS Code** with MCP extension
- **Claude Code (CLI)**
- **ChatGPT** with MCP connector
- **mcp-inspector** as debug tool
- **Custom scripts** via `curl` + JSON-RPC

Enter URL + bearer token from ForgeIEC Studio into the respective
client — done. Connecting to
[ChatGPT / Claude / local](/help/ai/providers/) is documented.

---

## Security: three layers, visible

The AI is secure by default. Three sequential layers must be
passed:

1. **Build-time gate** — the default distribution from the APT
   repo is read-only. Write actions require a separately built
   editor. That is a real separation, not a checkbox.
2. **Confirmation State Machine** — every write action returns
   `FORGE_ERR_CONFIRMATION_REQUIRED`, the operator confirms via
   `editor.confirm`. No silent background changes.
3. **Operator visibility** — every action visible in the chat log,
   audit log with timestamp.

Force settings (pin hardware outputs) are **explicitly not**
accessible via MCP — that remains operator authority through the
GUI.

More: [Security model](/help/ai/security/) and
[Architecture depth](/help/ai/architecture/).

---

## Anti-loop helpers — because LLMs are not perfect

LLMs get stuck in infinite loops when they don't understand an
error. ForgeIEC Studio addresses this with **actionable error
messages**: every compile error delivers not just "Expected := or
(" math, but the concrete MCP call to fix it. Example:

> "X is a Function Block — declare instance first.
> Action: project.write.add_variable scope_kind=pou iecType=TON"

Plus a configurable **tool-step limit** (default 10 steps per
user request) and a fast mode with **emergency stop button** (red
industrial mushroom button) for when the AI runs off anyway.

---

## What the commits delivered

The AI platform is not a big bang but a series of sprints building
on each other:

- **MCP-1**: Prompts in QSettings + editable system prompt
- **MCP-2**: Confirmation State Machine + project lifecycle
- **MCP-3a..i**: Tool families staggered — JSON-RPC, library, tasks,
  bellows, anvil, monitor, oscilloscope, catalog, codegen
- **MCP-3.5**: Multi-agent dock — 5 default personas
- **MCP-3.6**: Chat tab as internal MCP client (instead of
  external tool)
- **MCP-4a**: Remote bind + HTTPS + bearer auth per profile
- **MCP-4b**: Federation + trust (see
  [dedicated post](/news/federation-team-trust/))
- **MCP-6**: project.write.* Phase-2 + runtime.* + state-machine
  integration
- **MCP-8**: Namespace-aware writes (pou/gvl/bellows/anvil triplet)
- **MCP-9**: Persistence + diagnostics + triplet convention

Source: `documentation/architecture/mcp-platform-v1.md` (~2300 LOC
formal spec, RFC 2119 language).

---

## Where you use it

| Setup | What for |
|---|---|
| **Local coding** | Cloud LLM or local model, personas in the AI tab |
| **Code review** | Reviewer persona, read-only — no risk |
| **Commissioning** | Monitor persona on production PLC — observation only |
| **Onboarding** | Trainee persona, confirm every action individually |
| **CI build server** | Headless Studio + curl + JSON-RPC from the build script |
| **Multi-LLM cooperation** | GPT as critic, Claude as coder, each with its own persona |

---

## Where to read more

- [AI assistant user docs](/help/ai/)
- [Personas](/help/ai/agents/), [Daily operation](/help/ai/chat/),
  [What the AI can do](/help/ai/tools/)
- [Providers — ChatGPT, Claude, local](/help/ai/providers/)
- [MCP for application engineers](/help/mcp/programmers/)
- [MCP for IT + operations](/help/mcp/it/)
