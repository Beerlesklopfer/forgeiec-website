---
title: "Using constants and math functions"
summary: "Practical guide: when to declare constants yourself vs. load forgeiec_math, how to mix INT/REAL/LREAL safely, where rounding bites, and the common ST recipes (degrees↔radians, polar↔cartesian, dB-scaling, hysteresis, accumulators)."
weight: 28
construct_kind: "guide"
keywords: ["constants", "PI", "E", "SQRT", "SIN", "COS", "LN", "EXP", "REAL", "LREAL", "precision", "rounding", "drift"]
---

## Decide once: where do PI/E come from?

Before you write the first line that needs `PI` or `E`, decide:

| Situation                                                              | What to do                          |
|-------------------------------------------------------------------------|-------------------------------------|
| Code only ever runs in ForgeIEC                                         | Load `forgeiec_math` and use `PI`, `E`, … |
| Code must also build under CODESYS / Beckhoff / matiec                  | Declare `PI` yourself in a `VAR_GLOBAL CONSTANT` |
| You're not sure yet                                                     | Declare yourself — 1 line, zero coupling |

Don't mix the two ways in the same project — pick one and stick with it.

### Declaring constants yourself (portable)

```iec-st
(* In a dedicated GVL — visible from every POU *)
VAR_GLOBAL CONSTANT
    PI    : LREAL := 3.141592653589793;
    E     : LREAL := 2.718281828459045;
    SQRT2 : LREAL := 1.414213562373095;
END_VAR
```

Use one decimal that fits LREAL precision (15–17 digits).  Both your
compiler and CODESYS/Beckhoff will convert to the same nearest-LREAL
bit pattern, so your numerics are identical.

### Using `forgeiec_math` (ForgeIEC-only)

Add `forgeiec_math` to the project's library list.  Then `PI`, `E`,
`SQRT2`, `SQRT1_2`, `LN2`, `LN10`, `GOLDEN_RATIO`, `EULER_MASCHERONI`,
plus pre-computed `TWO_PI` and `PI_HALF` are all available everywhere
in ST code.  See the [constants reference](../constants/) for the
full table.

## Picking the right precision: REAL vs LREAL

| Type    | Precision               | Range                     | Use when                                        |
|---------|-------------------------|---------------------------|-------------------------------------------------|
| `REAL`  | ~7 decimal digits       | ±3.4·10³⁸                 | Single sensor reading, scaling output to PWM    |
| `LREAL` | ~15 decimal digits      | ±1.8·10³⁰⁸                | Anything with accumulators, multi-step math, PID|

Rule of thumb: **inputs and one-shot outputs can be `REAL`, anything
that integrates over time should be `LREAL`**.  Rounding in `REAL` is
about 30,000 times coarser than `LREAL` and accumulators show it
within minutes.

```iec-st
(* sensor → REAL is plenty *)
rTempC : REAL := REAL(iAdcRaw) * 0.0625;

(* integrator → LREAL or it drifts *)
rTotalLitres : LREAL := rTotalLitres + LREAL(rFlowLm) * 0.001;
```

## Mixing INT and REAL: explicit is safer

IEC 61131-3 does **not** auto-promote between integer and floating
types — you have to convert explicitly with `INT_TO_REAL`, `REAL_TO_INT`,
`DINT_TO_LREAL` etc.  matiec follows this strictly; vendors that do
auto-promotion are non-portable.

```iec-st
(* This is a type error — INT and REAL don't mix *)
rResult := iCount + 0.5;        (* compiler rejects *)

(* Correct — explicit promotion *)
rResult := INT_TO_REAL(iCount) + 0.5;

(* Inverse — explicit truncation *)
iRound := REAL_TO_INT(rResult);   (* truncates toward zero, not banker's round *)
```

See [type-conversion](../functions/type-conversion/) for the full family.

## Math functions: domain checks BEFORE you call

The IEC math functions don't raise exceptions — they return special
values that propagate silently through the rest of your code.

| Function | Bad input        | What you get                  | Effect downstream                            |
|----------|------------------|-------------------------------|----------------------------------------------|
| `SQRT`   | negative         | `NaN`                         | Every later op with NaN is NaN. PID dies.    |
| `LN`,`LOG`| 0                | `-∞`                          | `-∞ + 1.0 = -∞`. Outputs saturate.            |
| `LN`,`LOG`| negative         | `NaN`                         | Same as SQRT.                                 |
| `DIV`    | divisor = 0      | depending on type             | INT division crashes (Beremiz) or wraps; REAL gives ±∞ or NaN. |
| `EXP`    | very large       | `+∞`                          | `+∞ * 0` becomes NaN. Same downstream death. |
| `ASIN`,`ACOS`| outside [-1,1] | `NaN`                         | Same.                                         |

**Always range-check the input.**

```iec-st
(* Always *)
IF rIn >= 0.0 THEN
    rRoot := SQRT(rIn);
ELSE
    rRoot := 0.0;   (* or fallback / error flag *)
END_IF;

(* For ASIN/ACOS — clamp into the domain *)
IF rIn > 1.0 THEN
    rArc := PI_HALF;        (* or 0.0 from forgeiec_math *)
ELSIF rIn < -1.0 THEN
    rArc := -PI_HALF;
ELSE
    rArc := ASIN(rIn);
END_IF;
```

## Accumulators in cycle bodies

This is the single biggest source of "works in the lab, drifts in
production":

```iec-st
(* AVOID — every cycle re-rounds the multiplication *)
rPhase := rPhase + 2.0 * PI * rFreq * rDt;

(* BETTER — pre-compute the constant once *)
VAR
    K : LREAL := 2.0 * PI;   (* one-shot, stored bit-exact *)
END_VAR
rPhase := rPhase + K * rFreq * rDt;

(* BEST — use the pre-computed TWO_PI from forgeiec_math *)
rPhase := rPhase + TWO_PI * rFreq * rDt;
```

For the modulo step that brings `rPhase` back to `[0, 2π)` after every
cycle: don't use `MOD` on REAL/LREAL (defined only for integers); do
the subtraction yourself:

```iec-st
IF rPhase >= TWO_PI THEN
    rPhase := rPhase - TWO_PI;
END_IF;
```

## Common recipes

### Degrees ↔ radians

```iec-st
FUNCTION rRad : LREAL  VAR_INPUT rDeg : LREAL; END_VAR
    rRad := rDeg * PI / 180.0;
END_FUNCTION

FUNCTION rDeg : LREAL  VAR_INPUT rRad : LREAL; END_VAR
    rDeg := rRad * 180.0 / PI;
END_FUNCTION
```

Pre-compute `PI / 180.0` and `180.0 / PI` once if you call these in a
tight loop — same drift argument as `TWO_PI`.

### Polar ↔ cartesian

```iec-st
FUNCTION_BLOCK PolarToCart
    VAR_INPUT   rRho, rTheta : LREAL; END_VAR
    VAR_OUTPUT  rX, rY       : LREAL; END_VAR
    rX := rRho * COS(rTheta);
    rY := rRho * SIN(rTheta);
END_FUNCTION_BLOCK

FUNCTION_BLOCK CartToPolar
    VAR_INPUT   rX, rY        : LREAL; END_VAR
    VAR_OUTPUT  rRho, rTheta  : LREAL; END_VAR
    rRho   := SQRT(rX * rX + rY * rY);
    (* IEC has no ATAN2 — fold the quadrant by hand *)
    IF      rX > 0.0                    THEN rTheta := ATAN(rY / rX);
    ELSIF   rX < 0.0  AND  rY >= 0.0    THEN rTheta := ATAN(rY / rX) + PI;
    ELSIF   rX < 0.0  AND  rY <  0.0    THEN rTheta := ATAN(rY / rX) - PI;
    ELSIF   rX = 0.0  AND  rY >  0.0    THEN rTheta := PI_HALF;
    ELSIF   rX = 0.0  AND  rY <  0.0    THEN rTheta := -PI_HALF;
    ELSE    rTheta := 0.0;              (* (0,0) — undefined; pick 0 *)
    END_IF;
END_FUNCTION_BLOCK
```

### dB scaling (amplitude → dB and back)

```iec-st
(* 20 · log10(A/A_ref).  Use LN/LN10 if LOG10 isn't available *)
rDb := 20.0 * LN(rAmp / rRef) / LN10;

(* inverse: A = A_ref · 10^(dB/20) *)
rAmp := rRef * EXP(rDb / 20.0 * LN10);
```

### First-order low-pass (RC filter)

```iec-st
(* alpha = dt / (RC + dt);  smaller alpha = more smoothing *)
rAlpha := rDt / (rTauRC + rDt);
rFiltered := rFiltered + rAlpha * (rInput - rFiltered);
```

Pre-compute `rAlpha` outside the cycle if `rDt` and `rTauRC` are
constant — saves one DIV every cycle.

### Hysteresis with two thresholds

```iec-st
IF (NOT bOn)  AND (rValue >= rHigh) THEN bOn := TRUE;  END_IF;
IF       bOn  AND (rValue <  rLow ) THEN bOn := FALSE; END_IF;
```

No math constants needed — but a very common pattern that often gets
written backwards or with a single threshold and then mysteriously
chatters.

## Diagnostic checklist when math goes wrong

1. **NaN propagating** — find the first `SQRT`/`LN`/`ASIN` that got
   out-of-domain input.  Add a range check upstream.
2. **Drift in accumulators** — check whether you're using `REAL` where
   `LREAL` would be appropriate, and whether the constant in the
   multiplication is pre-computed.
3. **Cross-vendor mismatch** — check if you're relying on implicit
   `PI`/`E` from a vendor library.  Declare them yourself with explicit
   decimals.
4. **Integer overflow at boundary** — `INT(32767) + INT(1)` wraps to
   `-32768` in IEC.  Use `DINT` if the result range can exceed 16 bit.
5. **`MOD` on REAL** — not defined in IEC.  Subtract by hand or use
   `TRUNC` + multiplication.

## See also

- [Mathematical constants](../constants/) — the full table
- [Arithmetic functions](../functions/arithmetic/) — `SIN`, `COS`,
  `SQRT`, `LN`, `EXP` and friends
- [Type conversion](../functions/type-conversion/) — `INT_TO_REAL`,
  `REAL_TO_LREAL`, etc.
- [Selection functions](../functions/selection/) — `MIN`, `MAX`,
  `LIMIT` for the range-clamping patterns above
