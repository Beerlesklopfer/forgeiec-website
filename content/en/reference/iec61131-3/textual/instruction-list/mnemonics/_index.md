---
title: "IL mnemonics"
summary: "The full IL instruction set — accumulator-style mnemonics for arithmetic, bitwise, comparison, branch and FB calls. Deprecated in IEC 61131-3 third edition (2013) but matiec still parses it."
weight: 10
iec_chapter: "6.6 (second edition)"
construct_kind: "il-instruction"
keywords: ["IL", "instruction", "LD", "ST", "ADD", "SUB", "JMP", "CAL"]
---

## ⚠️ Deprecated

The third edition of IEC 61131-3 (2013) **removed** IL from
the standard. matiec still accepts IL for round-trip with
legacy projects, but new POUs should use ST.

If you have IL POUs in an inherited project, this page lists
the instruction set so you can read and migrate them. The
single-accumulator model is straightforward to translate to
ST: each `LD <var>` starts a new ST expression chain, each
arithmetic instruction extends the chain, and each `ST <var>`
terminates the chain with an assignment.

## The accumulator model

Every IL instruction operates on the **current result** (CR)
— a single implicit register. The CR's type is whatever the
last instruction set it to.

```text
LD  iA          (* CR := iA *)
ADD iB          (* CR := CR + iB *)
ST  iResult     (* iResult := CR *)
```

is equivalent to ST:

```iec-st
iResult := iA + iB;
```

## Load and store

| Mnemonic | Operand | Meaning |
|---|---|---|
| `LD` | `var` or literal | CR := operand |
| `LDN` | `var` (BOOL) | CR := NOT operand (BOOL only) |
| `ST` | `var` | var := CR |
| `STN` | `var` (BOOL) | var := NOT CR |
| `S` | `var` (BOOL) | If CR is TRUE: var := TRUE (set) |
| `R` | `var` (BOOL) | If CR is TRUE: var := FALSE (reset) |

## Arithmetic

| Mnemonic | Operand | Meaning |
|---|---|---|
| `ADD` | `var` or literal | CR := CR + operand |
| `SUB` | | CR := CR - operand |
| `MUL` | | CR := CR * operand |
| `DIV` | | CR := CR / operand |
| `MOD` | | CR := CR MOD operand |

## Bitwise / logical

| Mnemonic | Operand | Meaning |
|---|---|---|
| `AND`, `&` | | CR := CR AND operand |
| `ANDN`, `&N` | | CR := CR AND NOT operand |
| `OR` | | CR := CR OR operand |
| `ORN` | | CR := CR OR NOT operand |
| `XOR` | | CR := CR XOR operand |
| `XORN` | | CR := CR XOR NOT operand |
| `NOT` | | CR := NOT CR |

## Comparison

| Mnemonic | Operand | Meaning |
|---|---|---|
| `GT` | | CR := CR > operand |
| `GE` | | CR := CR >= operand |
| `EQ` | | CR := CR = operand |
| `NE` | | CR := CR <> operand |
| `LE` | | CR := CR <= operand |
| `LT` | | CR := CR < operand |

## Branch

| Mnemonic | Operand | Meaning |
|---|---|---|
| `JMP` | label | unconditional jump |
| `JMPC` | label | jump if CR is TRUE |
| `JMPCN` | label | jump if CR is FALSE |
| `RET` | | return from function/FB |
| `RETC` | | return if CR is TRUE |
| `RETCN` | | return if CR is FALSE |

Labels are written `label:` on their own line:

```text
LD     xMode
JMPC   skip
LD     iA
ADD    iB
ST     iResult
skip:  LD  xDone
       ST  xFlag
```

## Function and FB calls

| Mnemonic | Operand | Meaning |
|---|---|---|
| `CAL` | `instance(args)` | unconditional call of FB instance |
| `CALC` | | call if CR is TRUE |
| `CALCN` | | call if CR is FALSE |

Function calls use the function name directly with parentheses:

```text
LD     iA
ABS                        (* CR := ABS(iA) *)
ST     iAbs

LD     instance.OUT        (* read FB output *)
```

## Parenthesised expressions

`(` defers the operation until the matching `)`. Inside the
parens, the CR builds up an expression that's then combined
with the outer CR using the deferred operator:

```text
LD    iA
ADD   ( iB
        MUL iC )           (* CR := iA + (iB * iC) *)
ST    iResult
```

This is the IL equivalent of operator precedence — without
parens IL is strictly left-to-right.

## Migration to ST

The mechanical translation:

| IL pattern | ST equivalent |
|---|---|
| `LD a / ST b` | `b := a;` |
| `LD a / ADD b / ST c` | `c := a + b;` |
| `LD a / GT b / ST x` | `x := a > b;` |
| `LDN a / ST b` | `b := NOT a;` |
| `JMPC l1 ... l1:` | `IF cond THEN ... END_IF;` (refactor as needed) |
| `CAL inst(p := v)` | `inst(p := v);` (same syntax in ST) |

Most legacy IL POUs translate to a few-line ST equivalent. The
hardest cases are deeply nested parens with many `JMPC`
labels — those usually map to `IF/ELSIF` cascades or `CASE`.

## IEC reference

IEC 61131-3 **second** edition (2003), clause 6.5 — defined
the IL instruction set. The third edition (2013) removed IL.

## matiec conformance

matiec accepts IL per the second-edition spec. New code
should be written in ST.
