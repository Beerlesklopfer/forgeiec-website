---
title: "FB instances vs. function calls"
summary: "Function Blocks need an instance declaration first; functions are called directly. Two of the most common compile errors in ForgeIEC stem from confusing the two."
weight: 10
iec_chapter: "6.6.2.1, 6.6.2.2"
construct_kind: "call"
keywords: ["FB", "FUNCTION_BLOCK", "instance", "TON", "CTU", "VAR"]
llm_signals:
  - error_pattern: "is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "An FB type name is being called directly as if it were a function (e.g. `TON(IN:=x, PT:=t)` instead of `myTon(IN:=x, PT:=t)`). FBs need a per-instance storage struct because they hold state across scan cycles; calling the *type* doesn't carry any state and is rejected."
    fix_strategy: "Declare a POU-local variable of that FB type, then call **the instance variable** (not the type) in the body. The MCP tool `project.write.add_variable` with `scope_kind=pou`, `scope_name=<your POU>`, `iecType=<FB type>` does the declaration in one call. Then re-issue `set_text_body` calling the instance name."
    fix_example: |
      (* before — fails: TON is a Function Block — declare instance first *)
      TON(IN := xStart, PT := T#100ms);
      IF TON.Q THEN ... END_IF;

      (* after — declare instance, then call it *)
      VAR
          stepTimer : TON;
      END_VAR

      stepTimer(IN := xStart, PT := T#100ms);
      IF stepTimer.Q THEN ... END_IF;
  - error_pattern: "has no declared parameter list"
    where: "matiec"
    diagnosis: "A function (FUN) is being called with named parameters (`fc(p := v)`) but the function declaration uses positional parameters or the parameter names don't match. matiec accepts both forms but doesn't substitute one for the other."
    fix_strategy: "Look up the function's actual parameter list with `library.read_block(name)` — the response carries `parameters[]` with the canonical names and order. Then either match the named-parameter spelling exactly, or fall back to positional `fc(v)` syntax."
    fix_example: |
      (* before — fails: ABS has no declared parameter list named 'value' *)
      iAbsResult := ABS(value := -3);

      (* after — option A: positional *)
      iAbsResult := ABS(-3);

      (* after — option B: lookup gave parameter name 'IN' *)
      iAbsResult := ABS(IN := -3);
  - error_pattern: "FB output read on type, not on instance"
    where: "FStCompiler"
    diagnosis: "Output access goes through the **instance** (`stepTimer.Q`), not through the **type** (`TON.Q`). Same root cause as the first signal — the FB type has no state of its own."
    fix_strategy: "Replace `<FBType>.<output>` with `<instance>.<output>`. If no instance exists, declare one first (see the first signal's fix)."
    fix_example: |
      (* before — fails *)
      IF TON.Q THEN ... END_IF;
      (* after *)
      IF stepTimer.Q THEN ... END_IF;
---

## Definition

In IEC 61131-3 every callable thing is either a **Function**
(FUN) or a **Function Block** (FB). The two have the same call
syntax (`name(arg, …)` or `name(p := v, …)`) but completely
different storage semantics:

- A **Function** has no internal storage. The same `ABS(-3)`
  call would always return `3` regardless of how many times
  it was called before. Functions are pure mathematical
  mappings from inputs to a single typed return value.
- A **Function Block** has internal storage that lives across
  scan cycles. A `TON` (timer-on-delay) keeps its elapsed-time
  counter between cycles; a `CTU` (counter-up) keeps its
  count between cycles; a user-written `FUNCTION_BLOCK` keeps
  whatever VAR declarations it has between cycles.

Because of this difference, FBs cannot be "called" the way a
function is. You must first **declare an instance variable** of
the FB type — that creates one persistent storage struct per
instance — and then **call the instance**, which routes through
its struct.

## Syntax

### Function call (FUN)

```text
result := function_name ( arg_list );

arg_list := positional_args | named_args
positional_args := expr { ',' expr }
named_args := param_name ':=' expr { ',' param_name ':=' expr }
```

### FB instance declaration + call

```text
(* declaration in the POU's VAR section *)
VAR
    instance_name : FB_TYPE;
END_VAR

(* call in the POU body — note: instance_name, not FB_TYPE *)
instance_name ( input_list );

(* read outputs *)
... := instance_name . output_name ;
```

## Examples

### Function (FUN) — direct call, no declaration needed

```iec-st
iCount    : INT;
rDistance : REAL;

iCount    := ABS(-3);                  (* positional *)
rDistance := SQRT(IN := 2.0);          (* named — IN is the canonical pin *)
```

### Function Block (FB) — declare instance, then call instance

```iec-st
VAR
    stepTimer : TON;                   (* one persistent struct per instance *)
    edgeRise  : R_TRIG;
END_VAR

stepTimer(IN := xStart, PT := T#100ms);  (* call the INSTANCE, not TON *)
edgeRise(CLK := xButton);

IF stepTimer.Q THEN                     (* read outputs through the instance *)
    DoStuff();
END_IF;

IF edgeRise.Q THEN                      (* one-shot pulse on rising edge *)
    Counter := Counter + 1;
END_IF;
```

## Semantics

A function call:
- Evaluates its arguments once.
- Computes a return value.
- Has **no after-effects** — the next call with the same
  arguments produces the same result.

A function-block call:
- Evaluates its inputs.
- Mutates the instance struct (the timer increments, the edge
  detector latches the previous CLK, the counter advances).
- Updates the instance's outputs.
- The outputs remain readable until the next call to the same
  instance.

## IEC reference

- Functions: IEC 61131-3 third edition (2013), clause **6.6.2.1**.
- Function blocks: clause **6.6.2.2**.
- Both clauses live under "Calling functions and function
  blocks" (6.6.2).

## matiec conformance

matiec implements both call mechanisms exactly as the standard
requires. The two recurring pain points are documented above
in the `llm_signals` block:

- Calling an FB type (e.g. `TON(IN:=x, PT:=t)`) instead of an
  instance — caught by the local FStCompiler.
- Mixing positional / named arguments in a way that doesn't
  match the function's declared parameter list — caught by
  matiec.

## ForgeIEC notes

The Ackersteuerung-2026-05-14 deploy involved exactly this
pattern in `FB_MANUAL_TIME`:

```iec-st
VAR
    tonMt : TON;            (* per-step timer *)
END_VAR

tonMt(IN := TRUE, PT := tMtPerBed);
IF tonMt.Q THEN
    iMtStep := iMtStep + 1;
END_IF;
```

Note the instance name `tonMt` is what is called and what is
queried; the FB type `TON` never appears in the body.
