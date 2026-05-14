---
title: "POU model — PROGRAM, FUNCTION_BLOCK, FUNCTION"
summary: "The three Program Organisation Unit kinds. PROGRAM is what tasks execute; FUNCTION_BLOCK is the stateful reusable unit; FUNCTION is the pure mapping."
weight: 40
iec_chapter: "6.6.2"
construct_kind: "pou"
keywords: ["POU", "PROGRAM", "FUNCTION_BLOCK", "FUNCTION"]
llm_signals:
  - error_pattern: "FUNCTION cannot have VAR"
    where: "matiec"
    diagnosis: "An IEC 61131-3 FUNCTION has VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT, VAR_TEMP and the implicit return-value variable, but **no VAR block for state**. Functions are pure — they have no storage that survives between calls."
    fix_strategy: "Convert the FUNCTION to a FUNCTION_BLOCK if you need persistent state. FBs have full VAR support; the trade-off is the caller must declare an instance."
    fix_example: |
      (* before — fails *)
      FUNCTION FC_Counter : INT
          VAR_INPUT iIncrement : INT; END_VAR
          VAR iCount : INT; END_VAR     (* persistent state — illegal in FUN *)
          iCount := iCount + iIncrement;
          FC_Counter := iCount;
      END_FUNCTION

      (* after — convert to FB *)
      FUNCTION_BLOCK FB_Counter
          VAR_INPUT iIncrement : INT; END_VAR
          VAR_OUTPUT iCount : INT; END_VAR
          (* iCount is VAR_OUTPUT — persists per instance *)
          iCount := iCount + iIncrement;
      END_FUNCTION_BLOCK
---

## The three POU kinds

| Kind | Has state? | Has return value? | Called via | Stored where |
|---|---|---|---|---|
| **PROGRAM** | Yes (per program instance) | No | Task scheduler | Resources |
| **FUNCTION_BLOCK** | Yes (per FB instance) | No | Instance variable | Anywhere a variable can live |
| **FUNCTION** | **No** | Yes (single typed return) | Direct call | Nowhere — call is pure |

## PROGRAM

The top-level executable unit. A `PROGRAM` is what a `TASK`
actually runs — it's the IEC equivalent of a "main" function,
except a configuration can have many `PROGRAM` instances each
assigned to a different task.

```iec-st
PROGRAM PLC_PRG
    VAR
        iCycleCount : INT := 0;
        tonStartup : TON;
    END_VAR

    iCycleCount := iCycleCount + 1;
    tonStartup(IN := TRUE, PT := T#5s);

    IF tonStartup.Q THEN
        DoMainWork();
    END_IF;
END_PROGRAM
```

A program's `VAR` block persists across cycles like an FB's,
but unlike FBs, a `PROGRAM` is instantiated only via the
`CONFIGURATION` / `RESOURCE` / `TASK` mechanism (see
[configuration](../configuration/)) — you don't `myProgInst :
PLC_PRG;` in another POU's VAR block.

## FUNCTION_BLOCK

The stateful, reusable workhorse. An FB has:

- `VAR_INPUT` — read-only inputs.
- `VAR_OUTPUT` — outputs (read by the caller via the
  instance).
- `VAR_IN_OUT` — pass-by-reference parameters.
- `VAR` — internal state that persists between calls **per
  instance**.
- `VAR_TEMP` — scratch that resets at each call.

```iec-st
FUNCTION_BLOCK FB_Counter
    VAR_INPUT
        xCU : BOOL;
        iPV : INT;
    END_VAR
    VAR_OUTPUT
        xQ : BOOL;
        iCV : INT;
    END_VAR
    VAR
        xPrevCU : BOOL;     (* edge-detector state *)
    END_VAR

    IF xCU AND NOT xPrevCU THEN
        iCV := iCV + 1;
    END_IF;
    xPrevCU := xCU;
    xQ := iCV >= iPV;
END_FUNCTION_BLOCK
```

The caller declares an **instance** and calls **the
instance**:

```iec-st
VAR
    myCount : FB_Counter;     (* one persistent struct *)
END_VAR

myCount(xCU := xButton, iPV := 10);
IF myCount.xQ THEN ... END_IF;
```

See [textual/structured-text/function-calls/fb-instance-vs-function](../../textual/structured-text/function-calls/fb-instance-vs-function/)
for the full story.

## FUNCTION

A pure mapping from inputs to one typed return value. **No
internal state.** Same call with same inputs always returns
the same value.

```iec-st
FUNCTION FC_Clamp : INT
    VAR_INPUT
        iValue : INT;
        iMin : INT;
        iMax : INT;
    END_VAR
    (* No VAR block allowed — see llm_signals *)
    VAR_TEMP
        iWork : INT;     (* this IS allowed; resets each call *)
    END_VAR

    iWork := iValue;
    IF iWork < iMin THEN iWork := iMin; END_IF;
    IF iWork > iMax THEN iWork := iMax; END_IF;
    FC_Clamp := iWork;        (* assign to function name = return value *)
END_FUNCTION
```

The return value is set by assigning to the **function name**,
not via a `RETURN` statement. `RETURN` exits the function but
doesn't carry a value — the most-recent assignment to
`<FunctionName>` is what the caller receives.

Calling a FUNCTION needs no instance — see
[function-calls/_index](../../textual/structured-text/function-calls/).

## When to pick which

| Situation | POU kind |
|---|---|
| Task that runs every cycle | `PROGRAM` |
| Reusable building block with state (timer, counter, edge detector, sequencer) | `FUNCTION_BLOCK` |
| Pure transformation: one or more inputs → one output, no memory | `FUNCTION` |
| Need persistent counter / accumulator inside reusable code | `FUNCTION_BLOCK` (a FUNCTION can't keep state) |

## ForgeIEC POU types

ForgeIEC extends the IEC POU set with three "VarList" POUs
that don't have executable bodies:

- **GlobalVarList (GVL)** — IEC `VAR_GLOBAL` block, exposed as
  a POU for editor convenience.
- **AnvilVarList** — auto-generated per-bus-device variable
  list. See [textual/structured-text/variables-references](../../textual/structured-text/variables-references/).
- **TempVarList** — project-local scratchpad GVL.

These show up in the project tree alongside PROGRAM/FB/FUN
POUs but contribute only declarations, no executable code.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.2** —
"Function and function block declarations" plus clause **6.6.6**
for `PROGRAM`.

## matiec conformance

All three POU kinds implemented per the standard. The "no VAR
in FUNCTION" rule is matiec's most common rejection point for
code ported from CoDeSys (which sometimes accepts state in
functions).
