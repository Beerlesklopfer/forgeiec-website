---
title: "Daily operation"
summary: "Input, input history, emergency stop, fast mode, tool-step limit"
---

## The chat area

In the right-side editor dock sits the `AI Assistant` tab. Layout
from top to bottom:

1. **Persona tabs** — Blacksmith Master, Reviewer, Doc, …
2. **Server address + model selection** — where the AI runs, which
   model
3. **Conversation log** — chat history between you and the
   assistant
4. **Input field** at the bottom — type your question here
5. **Safety banner** (yellow with a red STOP button) — only visible
   when Fast mode is active

---

## Asking a question

Type your question into the input field and press **Enter**.

> "Create 16 BOOL variables `LED_00` through `LED_15` at addresses
> `%MX0.0` through `%MX1.7`, with Bellows export."

The assistant first breaks your request into steps, executes them,
asks back at each write action, and gives a final report.

---

## Input history — up / down arrows

Like in a Linux shell:

- **Up arrow** in the input field → bring back the last entry
- **Down arrow** → next-younger entry
- Saves typing when you want to vary a similar question

---

## Emergency stop — the red STOP button

When Fast mode is active (see next section), a **yellow safety
strip** appears at the bottom with a **red round STOP button** on
the right.

**Press it any time** the AI is doing something you don't want. It
interrupts **immediately**:

- The running model call
- All pending tool steps
- Any open confirmation questions are set to "cancel"

The button uses the classic industrial mushroom-button form factor:
large, red, easy to hit, always reachable.

---

## Fast mode (Danger Mode)

By default, ForgeIEC Studio asks a question at **every** AI write action.
That is safe but slow — if the AI is supposed to create 50 variables,
you click through 50 confirmations.

**In Fast mode** ForgeIEC Studio answers these questions **automatically
with "yes"**. The LLM loop can then run through without human
interruption. Recommended only for **test setups** or **experimental
iteration** — in production you should **leave it off**.

**How to switch:**

`Preferences → AI` → checkmark `Danger Mode — auto-confirm AI tool
calls`.

On enabling, an extra safety warning appears telling you this mode
**must not** run on a productive PLC. Confirm only if you understand
that.

When switching between personas, the mode is remembered per persona —
so you can keep the Blacksmith Master fast and the Trainee slow.

---

## Tool-step limit (max_tool_turns)

A single request from you can trigger **multiple tool calls** at the
assistant. Example: "Create a Knight Rider program" internally does:

1. Create POU `KnightRider`
2. Create 16 LED variables
3. Write POU body
4. Compile
5. Deploy
6. Start PLC

That is already 21 steps. To prevent the assistant from running off
in an infinite loop, there is a **step limit per request**.

**Default: 10 steps.** Enough for simple requests.

**Adjust** via `Preferences → AI → Max tool turns per user request`.
Allowed values: 1 to 1000.

**In Fast mode** the limit is **automatically disabled** — if you
already trust the AI, it should be able to finish a long job.

When the limit is reached, the assistant breaks cleanly and says:
"Tool-loop guard hit max N turns; aborted." You can then type
"continue" and it picks up from there.

---

## What to do if the AI gets lost?

Sometimes a model tries the same wrong thing three or four times.
Helpful:

- **STOP button** → break the loop cleanly
- **Reword** — shorter, more concrete, with addresses instead of
  names
- **Switch persona** — Reviewer sometimes finds the bug Blacksmith
  Master misses
- **Switch model** — if your local model is too small, a bigger
  model can solve the same task in one try

---

## Next

- [What the AI can do](/help/ai/tools/) — list of possible actions
- [Security model](/help/ai/security/) — details about Fast mode
- [Personas](/help/ai/agents/) — which character for which task
- [Back to the AI overview](/help/ai/)
