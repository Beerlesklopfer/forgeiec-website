---
title: "The personas in detail"
summary: "What each AI character may do, and when to pick which one"
---

## Why multiple personas?

A PLC programming environment needs **different viewpoints**:

- When coding, you want to create variables and compile quickly.
- When code-reviewing, you want **no** accidental changes.
- When commissioning, you only look at live values — not at the code.
- When onboarding a trainee, the AI should **ask for every step**,
  so the trainee sees what is happening.

Instead of constantly toggling the security profile, ForgeIEC ships
with **ready-made personas** — each with its own role and its own
permission tier.

You switch between them as tabs in the AI panel.

---

## The five personas

### Blacksmith Master — the foreman

- **When to pick?** Default for active programming.
- **What may it do?** Everything: create variables, write POU code,
  compile, upload, start/stop the PLC, observe values.
- **Caution:** It can bring a PLC into stop state. Confirmation
  questions are shown for every action (except in Fast mode, see
  [Daily operation](/help/ai/chat/)).

### Reviewer — the second pair of eyes

- **When to pick?** When you want your code looked over before
  deploying.
- **What may it do?** **Read only**: project variables, POU bodies,
  library blocks. It **cannot** create variables, **cannot** modify
  code, **cannot** trigger a deploy.
- **Safety benefit:** You can let it chat unattended — it **cannot
  break anything**, even with bad instructions.

### Doc — the documentarian

- **When to pick?** When you want to generate comments or a
  documentation file from finished code.
- **What may it do?** Read + write variable comments. **No** POU
  body changes, **no** deploy.
- **Typical use:** "Read my `MotorControl` POU and write a short
  comment for each variable describing what it does."

### Monitor — the observer

- **When to pick?** When you do diagnostics on a running plant
  WITHOUT any risk of changes.
- **What may it do?** **Only** read live values, fetch oscilloscope
  captures, show task statistics.
- **What may it NOT do?** No variable creation, no force settings,
  no code touching, no deploy.
- **Typical question:** "Why does `Motor_Ready` stay FALSE during
  startup? Look at the last 5 seconds on the oscilloscope."

### Trainee — for onboarding and first contact

- **When to pick?** When onboarding a new colleague — or when you
  yourself are using the AI assistant for the first time and want
  to see everything step by step.
- **What may it do?** In principle everything like Blacksmith
  Master.
- **What's different?** Fast mode is **always off** for this persona.
  Every single action requires your click confirmation. Even if the
  operator types "do it, do it, do it" in rapid succession, a
  question pops up after every step.

---

## Create your own character

You can customise the shipped personas or create new ones:

- **Right-click on a tab** → `Duplicate Profile`
- **Preferences → AI** → adjust the system prompt
  (e.g. "Always reply in German, terse technical style")

The **system prompt** is the text used to "prime" the AI on every
request. Here you can set style, language, level of detail, domain
knowledge.

---

## Which persona for which task?

| You want to … | Persona |
|---|---|
| Write a new program | Blacksmith Master |
| Code review before deploy | Reviewer |
| Documentation from finished code | Doc |
| Diagnose a running plant | Monitor |
| Onboard a trainee | Trainee |
| First steps with the assistant | Trainee, then Blacksmith Master |

---

## Next

- [Daily operation](/help/ai/chat/) — input tricks, emergency stop
- [What the AI can do](/help/ai/tools/) — actions overview
- [Back to the AI overview](/help/ai/)
