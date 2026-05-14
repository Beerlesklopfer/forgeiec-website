---
title: "Bit-shift functions"
summary: "SHL, SHR, ROL, ROR. WARNING: matiec emit-bug with SHL(BYTE#1, …) — use IF/ELSIF or CASE-of cascade instead. See the llm_signals."
weight: 50
iec_chapter: "Annex F.2.3"
construct_kind: "function"
keywords: ["SHL", "SHR", "ROL", "ROR", "bit-shift", "rotate"]
llm_signals:
  - error_pattern: "SHL was not declared in this scope"
    where: "gcc"
    diagnosis: "matiec emits broken C-code for `SHL(BYTE#1, INT_TO_UINT(x))`: it produces `data__->BYTE` (a struct-member access) instead of an integer literal cast for the typed-literal argument. The `SHL` symbol then is searched for in the runtime header but doesn't exist with that signature."
    fix_strategy: "Don't use SHL with a typed-literal first argument in matiec. Replace with an `IF/ELSIF` cascade or `CASE OF` over decimal literals — the dispatch is explicit, and matiec emits clean C for both."
    fix_example: |
      (* before — fails on PLC g++ compile *)
      bMask := SHL(BYTE#1, INT_TO_UINT(iStep));
      (* after — explicit dispatch *)
      IF iStep = 0 THEN bMask := INT_TO_BYTE(1);
      ELSIF iStep = 1 THEN bMask := INT_TO_BYTE(2);
      ELSIF iStep = 2 THEN bMask := INT_TO_BYTE(4);
      ELSIF iStep = 3 THEN bMask := INT_TO_BYTE(8);
      ELSIF iStep = 4 THEN bMask := INT_TO_BYTE(16);
      ELSIF iStep = 5 THEN bMask := INT_TO_BYTE(32);
      END_IF;
  - error_pattern: "'BYTE' has no member named 'BYTE'"
    where: "gcc"
    diagnosis: "Same SHL/typed-literal emit-bug, different symptom — the generated C tries to access `.BYTE` on the FB's data struct."
    fix_strategy: "Same fix as above: replace SHL with IF/ELSIF cascade or pre-computed constant table."
---

## ⚠️ matiec SHL emit-bug

Before reading the rest of this page: **`SHL(BYTE#1, …)` is
broken in matiec.** The C-code generator emits a `data__->BYTE`
struct-member access where it should emit an integer literal.
The local FStCompiler accepts the call; only the PLC-side g++
compile fails. See `llm_signals` for the workaround.

The bug only triggers when the first argument is a **typed
literal** like `BYTE#1`. Workarounds:

- Use an `IF/ELSIF` cascade or `CASE OF` over decimal literals
  (recommended — explicit, matiec-clean).
- Pre-compute the value with `INT_TO_BYTE(1)` and store in a
  local; pass the local to SHL. This may also work depending
  on the matiec version, but the IF cascade is reliable.

The same emit-bug doesn't affect `SHR`, `ROL`, `ROR` in our
testing — but the safe pattern is the same.

## SHL — shift left

`SHL(IN: ANY_BIT, N: UINT): ANY_BIT` — shifts `IN` left by
`N` positions; vacated bits are zero.

```iec-st
bResult := SHL(bByte, 2);   (* multiply by 4 *)
wResult := SHL(wWord, 8);   (* shift the low byte to the high byte *)
```

`IN` and result are the same `ANY_BIT` type
(`BYTE`/`WORD`/`DWORD`/`LWORD`). `N` is `UINT`.

Bits shifted off the high end are **lost** — there is no
"sticky" or carry behaviour.

## SHR — shift right

`SHR(IN: ANY_BIT, N: UINT): ANY_BIT` — shifts right; vacated
bits are zero (logical shift, not arithmetic).

```iec-st
bResult := SHR(bByte, 2);   (* divide by 4, unsigned *)
```

## ROL — rotate left

`ROL(IN: ANY_BIT, N: UINT): ANY_BIT` — bits shifted off the
high end wrap around to the low end.

```iec-st
bResult := ROL(2#1000_0001, 1);   (* → 2#0000_0011 *)
```

## ROR — rotate right

`ROR(IN: ANY_BIT, N: UINT): ANY_BIT` — bits shifted off the
low end wrap to the high end.

```iec-st
bResult := ROR(2#1000_0001, 1);   (* → 2#1100_0000 *)
```

## When NOT to use shifts

For **bit-mask construction by index** (the canonical
`1 << N` pattern), prefer one of:

- An `IF/ELSIF` cascade with explicit decimal literals (always
  matiec-safe).
- A `CASE OF` with decimal labels — but watch out for the
  hex-literal case-label quirk documented at
  [textual/structured-text/control-flow/case-statement](../../../textual/structured-text/control-flow/case-statement/).
- A const lookup table:

  ```iec-st
  VAR CONSTANT
      arrMask : ARRAY[0..7] OF BYTE := [1, 2, 4, 8, 16, 32, 64, 128];
  END_VAR

  bMask := arrMask[iStep];
  ```

For **bit-by-bit access** of a `BYTE`/`WORD`/`DWORD`/`LWORD`,
prefer the bit-access syntax over a shift+mask pattern:

```iec-st
xBit := bByte.3;       (* read bit 3 as BOOL — clean, type-checked *)
bByte.5 := TRUE;       (* write bit 5 *)
```

See [bitwise operators](../../../textual/structured-text/operators/bitwise/).

## IEC reference

IEC 61131-3 third edition (2013), Annex **F.2.3** —
"Bit-string functions" Table F.7.

## matiec conformance

`SHL` has the documented emit-bug with typed-literal first
arguments — see `llm_signals`. `SHR`, `ROL`, `ROR` work as
expected in matiec at the time of writing.

A future matiec++ or rustly backend (see
[News: open language backend](/news/language-backends-matiec-rustly/))
is expected to make this quirk go away.
