---
title: "Selection & jump (RETURN, EXIT, CONTINUE, GOTO)"
summary: "Statements that change the flow of execution outside the regular IF/CASE/loop structure."
weight: 60
iec_chapter: "6.6.3.7"
construct_kind: "control-flow"
keywords: ["RETURN", "EXIT", "CONTINUE", "GOTO"]
llm_signals:
  - error_pattern: "EXIT outside loop"
    where: "FStCompiler"
    diagnosis: "EXIT only makes sense inside a FOR/WHILE/REPEAT loop. Used outside, it has no target."
    fix_strategy: "Replace with RETURN if the goal is to leave the POU. Or restructure the surrounding code so the EXIT is genuinely inside a loop."
  - error_pattern: "GOTO is not standard ST"
    where: "matiec"
    diagnosis: "matiec does NOT implement GOTO. It was deprecated in IEC 61131-3 second edition and removed from the third edition. Some legacy code from older vendor toolchains still uses it."
    fix_strategy: "Restructure with IF/CASE/loop. Most uses of GOTO map to either EXIT (escape from a loop) or to a step-machine implemented via CASE-of-iStep."
---

## RETURN

Leaves the current POU immediately. In a `FUNCTION`, the
return value must have been assigned to the function name
already; otherwise it carries the type's default value.

```iec-st
PROGRAM PLC_PRG
    IF NOT xEnable THEN
        (* skip the rest of this scan *)
        RETURN;
    END_IF;
    DoMainWork();
END_PROGRAM
```

In an `FB`, RETURN simply ends the call; outputs keep their
last assigned values.

In a `FUNCTION`, RETURN ends the call; the value of the
function-name variable at the moment of RETURN is what the
caller receives.

```iec-st
FUNCTION FC_Clamp : INT
    VAR_INPUT iValue : INT; iMin : INT; iMax : INT; END_VAR
    IF iValue < iMin THEN
        FC_Clamp := iMin;
        RETURN;                  (* short-circuit *)
    END_IF;
    IF iValue > iMax THEN
        FC_Clamp := iMax;
        RETURN;
    END_IF;
    FC_Clamp := iValue;
END_FUNCTION
```

## EXIT

Terminates the **innermost enclosing loop** (`FOR`, `WHILE`,
or `REPEAT`) immediately. Execution continues with the
statement following the loop's `END_FOR` / `END_WHILE` /
`END_REPEAT`.

```iec-st
FOR i := 1 TO 100 DO
    IF arr[i] = TARGET THEN
        iFound := i;
        EXIT;          (* leave the FOR — i and any later code skipped *)
    END_IF;
END_FOR;
```

EXIT only escapes **one** level. Nested loops need an EXIT per
level, or a flag-and-break pattern:

```iec-st
xDone := FALSE;
FOR i := 1 TO 10 DO
    FOR j := 1 TO 10 DO
        IF matrix[i, j] = TARGET THEN
            xDone := TRUE;
            EXIT;
        END_IF;
    END_FOR;
    IF xDone THEN EXIT; END_IF;
END_FOR;
```

## CONTINUE

Skips the rest of the current loop iteration and advances to
the next. In `FOR`, the loop variable advances by `BY` (or
`+1`) and the next iteration starts. In `WHILE` / `REPEAT`,
the condition is re-tested.

```iec-st
FOR i := 1 TO 100 DO
    IF arr[i] = 0 THEN
        CONTINUE;       (* skip zero entries *)
    END_IF;
    iSum := iSum + arr[i];
END_FOR;
```

CONTINUE was introduced in IEC 61131-3 third edition (2013);
older matiec versions may not accept it. ForgeIEC's matiec
build does.

## GOTO — NOT in IEC 61131-3 third edition

The third edition (2013) **removed** the labelled `GOTO`
statement. matiec does not accept it. Legacy code from older
vendor toolchains that uses GOTO needs restructuring on import.

Common GOTO → standard-ST migrations:

| GOTO use | Replacement |
|---|---|
| Skip ahead inside a loop | `CONTINUE` |
| Escape a loop early | `EXIT` |
| Escape multiple loop levels | flag + EXIT per level |
| Multi-way dispatch on a value | `CASE` |
| Step machine | `CASE OF iStep` with iStep advanced by transitions |
| Error handling / cleanup | restructure with IF + RETURN |

## IEC reference

- `RETURN`, `EXIT`: clause **6.6.3.7** of IEC 61131-3 third
  edition (2013).
- `CONTINUE`: introduced in third edition; same clause.
- `GOTO`: deprecated in second edition, removed in third
  edition.

## matiec conformance

`RETURN`, `EXIT`, `CONTINUE` implemented per the standard. No
`GOTO` support — see the migration table above for the
common replacements.
