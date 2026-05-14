---
title: "Positional vs. named parameters"
summary: "IEC 61131-3 accepts both `fc(a, b)` and `fc(p1 := a, p2 := b)` — but the rules for which is allowed where are not symmetric. Mismatches are matiec's #1 source of cryptic call errors."
weight: 20
iec_chapter: "6.6.2.1, 6.6.2.2"
construct_kind: "call"
keywords: ["positional", "named", "parameters", "arguments", "FB", "function"]
llm_signals:
  - error_pattern: "has no declared parameter list"
    where: "matiec"
    diagnosis: "A function or FB call uses a parameter name (`p := v`) that doesn't appear in the callee's declaration. matiec accepts both positional and named, but doesn't auto-translate one form to the other and doesn't fuzzy-match parameter names."
    fix_strategy: "Look up the canonical parameter list with `library.read_block(name)` — the response gives the exact spelling and order. Then either match the names exactly, or fall back to positional syntax. Names are case-sensitive in matiec even though IEC says identifiers are case-insensitive."
    fix_example: |
      (* before — fails: ABS has no declared parameter list named 'value' *)
      iAbsResult := ABS(value := -3);

      (* after — option A: positional (always works for a 1-arg FUN) *)
      iAbsResult := ABS(-3);

      (* after — option B: named with the canonical parameter spelling *)
      iAbsResult := ABS(IN := -3);
  - error_pattern: "too few arguments"
    where: "matiec"
    diagnosis: "A positional call has fewer arguments than the function's declared parameters. Common when a function has been refactored to add a parameter and old call sites haven't been updated."
    fix_strategy: "Prefer the named-parameter form on multi-arg calls — it documents the call site against future refactoring (named args don't break when the parameter order changes)."
    fix_example: |
      (* before — refactored function gained a param *)
      result := MyFunc(a, b);
      (* after — named form survives reordering *)
      result := MyFunc(IN1 := a, IN2 := b, MODE := 0);
  - error_pattern: "mixed positional and named arguments"
    where: "matiec"
    diagnosis: "matiec rejects mixing `fc(a, p := v)` — once you use named-syntax in a call, all arguments must be named (or all must be positional)."
    fix_strategy: "Pick one form per call site and stick with it. Positional for short single-purpose calls (`ABS(-3)`); named for multi-arg FB invocations (`stepTimer(IN := xStart, PT := T#1s)`)."
    fix_example: |
      (* before — fails: mixed positional and named *)
      stepTimer(xStart, PT := T#100ms);
      (* after — all named *)
      stepTimer(IN := xStart, PT := T#100ms);
---

## Definition

Both forms are legal IEC 61131-3:

- **Positional**: `fc(a, b, c)` — arguments are matched to
  parameters by their position in the parameter list. Concise
  but fragile against parameter-list refactors.
- **Named**: `fc(IN1 := a, IN2 := b, MODE := c)` — arguments are
  matched by name. Verbose but stable across refactors and
  self-documenting.

The two forms cannot be mixed within a single call.

## Syntax

### Positional

```text
result := fname ( expr1 , expr2 , ... );
```

Arguments must appear in the order declared on the function /
FB. Trailing optional inputs may be omitted (matiec extension —
the IEC standard requires all positional arguments to be
present).

### Named

```text
result := fname ( param1 := expr1 , param2 := expr2 , ... );
```

Arguments may appear in any order. Optional inputs may be
omitted. The parameter name on the left of `:=` must match the
callee's declaration **exactly** (case-sensitive in matiec).

## When to prefer which

| Situation | Recommended form |
|---|---|
| Single-argument standard function (`ABS`, `SQRT`, `NOT`) | Positional — concise, no ambiguity |
| Multi-argument standard function with stable parameter list (`SEL`, `MUX`, `LIMIT`) | Either; named for clarity in non-trivial cases |
| Multi-argument FB call (`TON`, `CTU`, `RS`) | **Named** — the parameter list (IN/PT/Q/ET) is meaningful and the order is non-obvious to a reader |
| User-written FB or function | **Named** — defends the call site against later parameter-list refactors |
| Existing call site under maintenance | Match the surrounding style |

## Examples

```iec-st
(* Positional — concise, fine for single-arg standard FUNs *)
iAbs    := ABS(-3);
rRoot   := SQRT(2.0);
xNotted := NOT xFlag;

(* Named — multi-arg FB, documents itself *)
stepTimer(IN := xStart,
          PT := T#100ms);

(* Mixed — IEC-illegal, matiec rejects *)
(* ✗ stepTimer(xStart, PT := T#100ms);  *)

(* Both forms work; pick named for FBs by default *)
edgeRise(CLK := xButton);              (* named *)
edgeFall(xButton);                     (* positional — also legal *)
```

## IEC reference

- Calling functions: clause **6.6.2.1** of IEC 61131-3 third
  edition (2013).
- Calling function blocks: clause **6.6.2.2**.

## matiec conformance

matiec accepts both forms as required. Two strict points worth
flagging:

1. **No mixing** within one call. matiec rejects
   `fc(a, p := v)` even though some vendor compilers accept it.
2. **Case-sensitive parameter names** in the named form.
   `stepTimer(in := x, pt := t)` is rejected even though IEC
   identifiers are case-insensitive in general. Always match
   the spelling reported by `library.read_block`.

## ForgeIEC notes

- The MCP tool `library.read_block(name)` returns the
  canonical parameter list for any FB or function. Use it
  before writing a multi-arg call to look up the exact
  parameter spelling, especially for built-ins like `TON`
  (parameters: `IN`, `PT`, `Q`, `ET`) or for user FBs whose
  parameter list might have changed since the last call site
  was written.
- The auto-completion in the ForgeIEC editor suggests
  parameter names in named form by default. If you typed a
  positional argument and hit `Tab`, the completion converts
  to named.
