---
title: "Function and FB calls"
summary: "Calling a Function (FUN) versus invoking a Function Block (FB) instance — two different mechanisms with two different syntactic forms."
weight: 30
iec_chapter: "6.6.2"
construct_kind: "call"
keywords: ["function", "function block", "FB", "FUN", "call", "invoke"]
---

## Function and FB calls

Structured Text has **two different call mechanisms** that are
easy to confuse and that produce two of the most common
beginner-and-LLM compile errors. Distinguishing them before
writing any call is the single most useful habit you can build:

| Aspect | Function (FUN) | Function Block (FB) |
|---|---|---|
| Has internal state? | **No** — pure function | **Yes** — instance carries state across cycles |
| Declared with | `FUNCTION foo : RETURN_TYPE` | `FUNCTION_BLOCK foo` |
| Used in code by | direct call: `foo(IN := x)` | first declare instance, then **call the instance**: `foo_inst(IN := x)` |
| Returns | a value via the function name | values via output pins of the instance |
| Example | `ABS(-3) → 3`, `SQRT(2.0) → 1.41…` | `TON`, `CTU`, `R_TRIG`, `RS`, `SR` and any user-written `FUNCTION_BLOCK` |
| Storage | none — call disappears after the cycle | one struct per declared instance, lives for the program's life |

### Quick decision tree

1. Does the operation need to **remember** something between
   one scan cycle and the next (an elapsed time, a counter
   value, a previous edge)? → It is a **Function Block**.
   Declare an instance variable first; then call the instance.
2. Otherwise it is probably a **Function**. Call it directly.
3. If you don't know which one a name is, look it up:
   `library.read_block("name")` — the response carries
   `kind: "FB"` or `kind: "FUN"`.

---

## Sub-pages

- **[FB instances vs. function calls](fb-instance-vs-function/)**
  — the canonical pattern for declaring an FB instance, plus
  the most common LLM error
  *"X is a Function Block — declare instance first"* and its
  one-line fix via `project.write.add_variable`.
- **[Positional vs. named parameters](positional-vs-named/)**
  — both forms are legal IEC 61131-3 but the rules for which
  is allowed where (functions vs FBs, libraries vs project)
  are subtle and produce *"has no declared parameter list"*
  errors when mixed up.

## ForgeIEC notes

- The library catalogue (`library.list_blocks` MCP tool) marks
  every entry as either FB or FUN; never guess based on the
  name alone. A user-written `FB_MANUAL_TIME` and a built-in
  `TON` are both FBs; a user-written `FC_GetKcValue` and a
  built-in `ABS` are both functions. The `FB_` / `FC_`
  prefix is project convention only.
- The MCP tool `project.write.add_variable` with
  `iecType: "TON"` (or any other FB type) creates the
  instance variable. The tool returns
  `FORGE_ERR_FB_INSTANCE_AS_LOCAL` when an FB instance is
  declared at the wrong scope (e.g. as a function-local in a
  `FUNCTION` POU, which has no persistent storage).
