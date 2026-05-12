---
title: "The AI assistant in ForgeIEC Studio"
summary: "How to use the built-in AI assistant for programming, diagnostics and commissioning"
---

## What is it?

ForgeIEC Studio ships with a built-in **AI assistant** — directly
in the main window, in the right-side tab `AI Assistant`. You can
talk to it in plain English (or German), and it can **operate
ForgeIEC Studio itself**:

- Create variables and assign addresses
- Write or modify POU code (Structured Text)
- Compile programs and deploy them to the PLC
- Watch live values while the PLC runs
- Capture time series on the oscilloscope

The assistant does **not have to** be a cloud service — it can run
**entirely on your own machine**, no internet required, using a
local AI program (e.g. LM Studio or llama.cpp server).

---

## Several characters for different tasks

The assistant comes with **multiple personas** — each with its own
job and its own permission profile. You switch between them as
tabs in the AI panel:

| Persona | What it does |
|---|---|
| **Blacksmith Master** | The foreman — writes code, compiles, deploys. Default for active development. |
| **Reviewer** | Reads your code and suggests improvements. Changes nothing on its own. |
| **Doc** | Writes comments and descriptions for your program. |
| **Monitor** | Only observes the running PLC — perfect for diagnostics. No changes possible. |
| **Trainee** | Same as the Foreman, but **every** action must be confirmed by you individually. For onboarding new staff or first tests. |

Details: [The personas in detail](/help/ai/agents/).

---

## Safety — the short version

The AI assistant **cannot accidentally** damage your running plant.
Three layers protect you:

1. **The default install is safe.** When you install ForgeIEC fresh
   from the APT repository, the AI can **only read**. Creating
   variables, compiling, and deploying are all **switched off**.
2. **Enabling has to be deliberate.** To allow write actions, you
   have to install a special version of ForgeIEC Studio — that is
   a real hardware-like separation, not a checkbox someone clicks
   by accident.
3. **The operator decides every action.** Even in the enabled
   version, ForgeIEC Studio asks a question for **every** change:
   > "Add `Position` variable with address `%MD100`? (yes / cancel)"
   Only with your confirmation does it actually happen.

More: [Security model](/help/ai/security/).

---

## Getting started

1. **Start ForgeIEC Studio** and select the `AI Assistant` tab in
   the right-side dock.
2. **Enter the server address** — where is your AI program running?
   - Locally on the same machine: usually
     `http://localhost:1234/v1` (LM Studio default).
   - On the company network: the address your IT gave you.
3. **Select the model** in the right drop-down — e.g.
   `qwen3-coder-30b`, `gpt-4o-mini`, `claude-opus-4-7`.
4. **Pick a persona** — for the first session, **Blacksmith Master**
   is right.
5. **Send a first request**, in plain English:
   > "Create a variable `Pressure_1` as REAL at address `%MD200`.
   > With Bellows export."

The assistant will create the variable, ask a confirmation question
("yes / cancel"), and after your approval it appears in the
Variables tab.

---

## Further topics

- [The personas in detail](/help/ai/agents/) — what each character
  may concretely do
- [Daily operation](/help/ai/chat/) — input tricks, emergency
  stop, fast mode
- [What the AI can do](/help/ai/tools/) — actions overview in plain
  terms
- [Connecting multiple workstations](/help/ai/team/) — Team mode,
  taking on coworkers, the trust chain
- [Security model](/help/ai/security/) — how the protection works
  in detail

---

<div style="text-align:center; padding: 2rem;">

**The AI is a tool. You decide.**

blacksmith@forgeiec.io

</div>
