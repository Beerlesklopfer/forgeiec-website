---
title: "TON — Timer-On-Delay"
summary: "Timer that delays a TRUE output until its IN input has been TRUE continuously for the preset time PT."
weight: 10
iec_chapter: "Annex F.7.1"
construct_kind: "function-block"
keywords: ["TON", "timer", "delay", "PT", "ET", "IN", "Q"]
llm_signals:
  - error_pattern: "TON is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "TON is being called as if it were a function. TON is a function block — it has internal state (the elapsed counter) that has to live somewhere across scan cycles."
    fix_strategy: "Add a POU-local of type TON via `project.write.add_variable scope_kind=pou iecType=TON`, then call the instance variable in the body."
    fix_example: |
      (* before — fails *)
      TON(IN := xStart, PT := T#100ms);
      IF TON.Q THEN ... END_IF;

      (* after *)
      VAR
          stepTimer : TON;
      END_VAR

      stepTimer(IN := xStart, PT := T#100ms);
      IF stepTimer.Q THEN ... END_IF;
  - error_pattern: "argument PT of TON has type INT, expected TIME"
    where: "matiec"
    diagnosis: "The PT (preset time) input expects a `TIME`-typed value. Passing an integer literal (`100`) or an INT variable triggers a type mismatch."
    fix_strategy: "Use a `TIME` literal: `T#100ms`, `T#5s`, `T#1m30s`, `T#1d12h`. Or declare a local `tStep : TIME := T#100ms;` and pass that. Never pass a bare integer."
    fix_example: |
      (* before — fails *)
      stepTimer(IN := xStart, PT := 100);
      (* after *)
      stepTimer(IN := xStart, PT := T#100ms);
  - error_pattern: "Q never goes TRUE"
    where: "runtime"
    diagnosis: "The TON output Q stays FALSE forever even though IN is observed TRUE. Two common causes: (a) IN is not actually TRUE for the entire PT period (it briefly drops, resetting the timer), or (b) the call is conditional on something that prevents the FB from being ticked every cycle."
    fix_strategy: "Call the instance UNCONDITIONALLY every cycle and gate behaviour on its outputs, not on whether to call it. Verify with `monitor.read_value` that `IN` is genuinely TRUE for the full duration."
    fix_example: |
      (* before — wrong: TON only ticks when xStart is TRUE,
         so Q never sees a continuous PT period *)
      IF xStart THEN
          stepTimer(IN := TRUE, PT := T#1s);
      END_IF;
      IF stepTimer.Q THEN ... END_IF;

      (* after — call every cycle, gate IN on the condition *)
      stepTimer(IN := xStart, PT := T#1s);
      IF stepTimer.Q THEN ... END_IF;
---

## Definition

`TON` ("Timer On-delay") is the canonical IEC 61131-3 delay
timer. After its `IN` input goes `TRUE` the timer starts
counting; after `PT` of continuous `IN = TRUE`, the output
`Q` goes `TRUE` and stays `TRUE` until `IN` returns to
`FALSE`. If `IN` drops to `FALSE` before `PT` is reached,
the timer resets and `ET` snaps back to `T#0s`.

Mnemonic: `Q` is **delayed-on**. Use `TON` whenever you want
"do X after Y has been true for Z time".

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `IN` | `BOOL` | Start the timer when this goes TRUE; reset it when it goes FALSE |
| Input | `PT` | `TIME` | Preset time — how long `IN` must stay TRUE before `Q` fires |
| Output | `Q` | `BOOL` | TRUE once `IN` has been TRUE continuously for at least `PT` |
| Output | `ET` | `TIME` | Elapsed time since `IN` went TRUE (capped at `PT`) |

## Syntax

```iec-st
VAR
    stepTimer : TON;
END_VAR

stepTimer(IN := <bool_expr>,
          PT := <time_expr>);

(* read outputs through the instance *)
... := stepTimer.Q;
... := stepTimer.ET;
```

## Examples

### Simple debounce

```iec-st
VAR
    debounceBtn : TON;
    xButtonRaw  : BOOL;       (* hardware input, may bounce *)
    xButtonOk   : BOOL;       (* clean signal for application code *)
END_VAR

(* Call EVERY cycle — gate the trigger on IN, not on whether to call *)
debounceBtn(IN := xButtonRaw, PT := T#20ms);
xButtonOk := debounceBtn.Q;
```

### Step sequence (per the Ackersteuerung pattern)

```iec-st
VAR
    tonMt    : TON;
    iMtStep  : INT := -1;
    tMtPerBed: TIME := T#10m;
END_VAR

(* When the FB is "running" on this step, run the timer.
   When the timer expires, advance the step and reset the timer. *)
IF xMtRunning THEN
    tonMt(IN := TRUE, PT := tMtPerBed);
    IF tonMt.Q THEN
        tonMt(IN := FALSE, PT := tMtPerBed);   (* reset the timer *)
        iMtStep := iMtStep + 1;
    END_IF;
ELSE
    tonMt(IN := FALSE, PT := tMtPerBed);
END_IF;
```

The trick in the second example is the **explicit reset call**
`tonMt(IN := FALSE, …)` after `Q` fires. Without that, the
timer would re-trigger on the very next cycle (because `IN` is
still `TRUE`) and immediately re-fire `Q`, looking like a
free-running pulse train.

## Semantics

Per IEC 61131-3 Annex F.7.1, evaluated on every call:

```
when IN goes FALSE → TRUE   (rising edge): start counting from 0
when IN is TRUE              and not yet at PT: ET := ET + cycle_time
when ET reaches PT                              : Q := TRUE
when IN goes TRUE → FALSE                       : Q := FALSE; ET := T#0s
```

`Q` is `TRUE` for as long as `IN` remains `TRUE` after the
preset has been reached. There is no "one-shot" mode — for
that, use `TP` (timer pulse).

`ET` is monotonically increasing within one continuous-IN
period and is capped at `PT` (it does not keep growing past
the preset).

## IEC reference

IEC 61131-3 third edition (2013), **Annex F (normative),
section F.7.1** — TON timer FB.

## matiec conformance

matiec implements TON exactly per the standard. The runtime
counter resolution is the task cycle: a TON with
`PT := T#1ms` running in a 20 ms task will fire `Q` after
**one** full task cycle (i.e. after 20 ms), not after the
nominal 1 ms. Monitor cadence rule: see the
[Sampling rule for correct interpretation](#) note in the
ForgeIEC monitor docs.

## ForgeIEC notes

- The MCP `library.read_block("TON")` tool returns the pin
  list shown above. Use it before writing a TON call to confirm
  the parameter names (case-sensitive in matiec).
- The `monitor.snapshot` tool reports `Q` and `ET` of any TON
  instance whose enclosing POU has `monitor_enabled=true` on
  the FB-instance variable. Useful to diagnose
  *"Q never goes TRUE"* situations live.
- Project memory `feedback_quantitative_tests`: any change
  to a TON-driven sequence needs a measuring capture+diff
  script, not "looks ok in the editor". TON behaviour at scan
  cycle N is non-trivially coupled to the cycle period.
