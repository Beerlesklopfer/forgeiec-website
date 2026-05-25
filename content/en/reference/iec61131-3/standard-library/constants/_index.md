---
title: "Mathematical constants"
summary: "PI, E, SQRT2, GOLDEN_RATIO and friends. Not in the IEC 61131-3 core — every vendor ships them differently. Make your ST code explicit about which constants it expects."
weight: 25
iec_chapter: "— (vendor extension; IEC §2.5.1 has the functions but no constants)"
construct_kind: "constant"
keywords: ["PI", "E", "SQRT2", "SQRT1_2", "LN2", "LN10", "GOLDEN_RATIO", "EULER_MASCHERONI", "TWO_PI", "PI_HALF"]
llm_signals:
  - error_pattern: "PI is not defined"
    where: "matiec"
    diagnosis: "IEC 61131-3 does not define PI as a built-in constant. The standard ships the *functions* (SIN/COS/LN/EXP) but expects you to provide your own constant. CODESYS Standard.lib, OSCAT, Beckhoff Tc2_Math and ForgeIEC each define it themselves, and the names + scopes differ."
    fix_strategy: "Either declare PI in a VAR_GLOBAL CONSTANT block in your project, or load the vendor library that provides it. Don't assume PI exists implicitly."
    fix_example: |
      (* portable — works on any IEC compiler *)
      VAR_GLOBAL CONSTANT
          PI : LREAL := 3.141592653589793;
      END_VAR

      FUNCTION rArea : LREAL
          VAR_INPUT rRadius : LREAL; END_VAR
          rArea := PI * rRadius * rRadius;
      END_FUNCTION
  - error_pattern: "rPhase drifts away from 0 after thousands of cycles"
    where: "runtime"
    diagnosis: "Computing `2.0 * PI` (or `PI / 2.0`) by multiplication introduces a one-ULP rounding every time. Over thousands of cycles this accumulates and a SIN-based wave drifts from zero crossings."
    fix_strategy: "Use the dedicated TWO_PI / PI_HALF constants if your library provides them. They store the pre-computed value bit-exact instead of re-doing the multiplication every cycle."
    fix_example: |
      (* avoid — one ULP rounding per cycle, drift over time *)
      rPhase := rPhase + 2.0 * PI * rFreq * rDt;

      (* better — bit-exact pre-computed *)
      rPhase := rPhase + TWO_PI * rFreq * rDt;
  - error_pattern: "Identical formula gives different result vs CODESYS"
    where: "cross-vendor"
    diagnosis: "Your code uses an implicit PI but the LREAL bit pattern your vendor stores for PI differs from the one another vendor uses. Tiny precision differences propagate through SIN/COS calls and produce different output."
    fix_strategy: "Stop relying on implicit PI. Declare it yourself with the EXACT decimal you want — both targets then converge to the same nearest-LREAL representation."
---

## Why this page exists

IEC 61131-3 §2.5.1 specifies mathematical *functions* — `SIN`, `COS`, `SQRT`,
`LN`, `EXP`, and friends — but **does not specify any constants**.  PLC code
that needs `π` or `e` therefore depends on whichever vendor library defines
them, and the libraries disagree:

| Vendor                 | Where PI comes from   | Notes                                      |
|------------------------|------------------------|--------------------------------------------|
| CODESYS Standard.lib   | global `VAR CONSTANT`  | Just `PI` (LREAL). No `E`, no `SQRT2`.    |
| CODESYS OSCAT          | OSCAT_BASIC library    | `PI`, `EULER`, `GOLDEN_RATIO`, more.       |
| Beckhoff Tc2_Math      | global constants       | Named `LREAL_PI` and `REAL_PI`.            |
| matiec / Beremiz       | nothing                | You must declare them yourself.            |
| **ForgeIEC**           | `forgeiec_math` lib    | All ten constants below; opt-in.           |

ST code that should run on more than one of these must be **explicit** about
where its constants come from.

## Available constants in `forgeiec_math`

When you add `forgeiec_math` to your project's library list, the following
names become available everywhere in ST code:

| Symbol              | Approximate value  | Type   |
|---------------------|--------------------|--------|
| `PI`                | 3.141592653589793  | LREAL  |
| `TWO_PI`            | 6.283185307179586  | LREAL  |
| `PI_HALF`           | 1.570796326794897  | LREAL  |
| `E`                 | 2.718281828459045  | LREAL  |
| `SQRT2`             | 1.414213562373095  | LREAL  |
| `SQRT1_2`           | 0.707106781186548  | LREAL  |
| `LN2`               | 0.693147180559945  | LREAL  |
| `LN10`              | 2.302585092994046  | LREAL  |
| `GOLDEN_RATIO`      | 1.618033988749895  | LREAL  |
| `EULER_MASCHERONI`  | 0.577215664901533  | LREAL  |

All values are stored at the highest precision LREAL allows.  You can
assign them straight into a REAL variable and the compiler does the
narrowing for you:

```iec-st
VAR
    rPiR  : REAL  := PI;     (* narrows to REAL precision *)
    rPiLR : LREAL := PI;     (* full LREAL precision *)
END_VAR
```

## Common patterns

### Circle area

```iec-st
FUNCTION rArea : LREAL
    VAR_INPUT  rRadius : LREAL; END_VAR
    rArea := PI * rRadius * rRadius;
END_FUNCTION
```

### Sine wave with stable phase

```iec-st
VAR
    rPhase : LREAL := 0.0;
    rFreq  : LREAL := 50.0;     (* Hz *)
    rDt    : LREAL := 0.001;    (* 1 ms cycle *)
    rOut   : LREAL;
END_VAR

(* Use TWO_PI directly — avoids one ULP of rounding per cycle.   *)
(* That difference accumulates over thousands of cycles and      *)
(* shows up as visible drift in long-running control loops.       *)
rPhase := rPhase + TWO_PI * rFreq * rDt;
IF rPhase >= TWO_PI THEN
    rPhase := rPhase - TWO_PI;
END_IF;
rOut := SIN(rPhase);
```

### Degree-to-radian conversion

There is no `DEG_TO_RAD` function — write it by hand:

```iec-st
FUNCTION rRad : LREAL
    VAR_INPUT  rDeg : LREAL; END_VAR
    rRad := rDeg * PI / 180.0;
END_FUNCTION
```

### Logarithmic compression

```iec-st
(* dB = 20 · log10(amplitude) — use LN and LN10 from the library *)
rDb := 20.0 * LN(rAmplitude) / LN10;
```

## Don't write `2.0 * PI` — use `TWO_PI`

`2.0 * PI` is one floating-point multiplication every time it's
evaluated, and IEEE-754 rounds the result to the nearest representable
LREAL.  That rounding is the same bit each cycle, so it's repeatable —
but a long-running phase accumulator using `2.0 * PI` will drift
visibly compared to one using the pre-computed `TWO_PI` constant.

For one-shot uses inside an expression the difference is invisible.
For accumulators inside `PROGRAM`-cycle bodies, always prefer the
pre-computed form.

## Portability notes

- If your code must also compile under CODESYS Standard.lib, declare
  the constants you actually use in a `VAR_GLOBAL CONSTANT` block.
  Both compilers will then converge on the same LREAL bit pattern (the
  decimal `3.141592653589793` has a unique nearest-LREAL).
- If your code must also compile under matiec, never write `2.0 * PI`
  expecting library-supplied `PI` — matiec ships no constants at all.
- The `forgeiec_math` library is **opt-in**.  Without loading it, the
  compiler will reject `PI`/`E`/etc. with the IEC-conformant error
  *"undefined identifier"* — no magic, no surprises.

## See also

- [Arithmetic functions](../functions/arithmetic/) — `SIN`, `COS`, `SQRT`,
  `LN`, `EXP` and friends.  These *are* in the IEC core.
- [Type conversion](../functions/type-conversion/) — `REAL_TO_LREAL`,
  `LREAL_TO_REAL` when you mix precisions.
