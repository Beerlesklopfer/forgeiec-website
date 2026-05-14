---
title: "Iteration (FOR / WHILE / REPEAT)"
summary: "Loops in ST. Three forms — counter-driven (FOR), condition-driven (WHILE/REPEAT). EXIT and CONTINUE break out / skip ahead."
weight: 50
iec_chapter: "6.6.3.4–6.6.3.7"
construct_kind: "control-flow"
---

## Iteration

Three loop constructs in IEC 61131-3 ST:

- **[`FOR`](for-loop/)** — counter-driven. Iterate a known
  number of times with a controlled loop variable. Use when
  the iteration count is computable upfront.
- **[`WHILE`](while-loop/)** — pre-test condition. Loop body
  may run zero times if the condition is `FALSE` on entry.
- **[`REPEAT`](repeat-loop/)** — post-test condition. Loop body
  always runs at least once.

Plus two flow-control statements that work inside any loop:

- **`EXIT`** — terminates the innermost enclosing loop
  immediately.
- **`CONTINUE`** — skips to the next iteration of the innermost
  enclosing loop.

## Loops on a PLC: scan-cycle hazard

Loops in PLC code have a special concern that desktop
programmers don't worry about: **a long-running loop blocks
the scan cycle**. If your `WHILE` runs for 50 ms in a 20 ms
task, you've already missed a deadline before the next scan
even starts. Outputs don't update; live monitoring stops; the
PLC may be flagged as overrun by the runtime.

Two consequences:

1. **Bound every loop**. A `WHILE x DO ... END_WHILE` without
   a counted exit clause is a code smell on a PLC. Add a
   safety-counter:

   ```iec-st
   iSafetyCount := 0;
   WHILE NOT xDone AND iSafetyCount < 100 DO
       (* work *)
       iSafetyCount := iSafetyCount + 1;
   END_WHILE;
   ```

2. **Prefer step-machines over long loops**. If the work would
   take many iterations, model it as an SFC (or a hand-rolled
   step counter) and do one iteration per scan. The PLC is a
   cyclic executor — work with the cycle, not against it.

## EXIT and CONTINUE

```iec-st
FOR i := 1 TO 100 DO
    IF arr[i] = TARGET THEN
        iFound := i;
        EXIT;            (* leave the loop early *)
    END_IF;
END_FOR;

FOR i := 1 TO 100 DO
    IF arr[i] = 0 THEN
        CONTINUE;        (* skip rest of body, advance i *)
    END_IF;
    iSum := iSum + arr[i];
END_FOR;
```

`EXIT` only leaves the **innermost** enclosing loop; nested
loops need an `EXIT` per level (or a flag-and-break pattern).
There is no `EXIT 2` form in IEC 61131-3.

## IEC reference

- `FOR`: clause **6.6.3.4**.
- `WHILE`: clause **6.6.3.5**.
- `REPEAT`: clause **6.6.3.6**.
- `EXIT`: clause **6.6.3.7**.

## matiec conformance

matiec implements all three loop constructs and `EXIT` /
`CONTINUE` per the standard.
