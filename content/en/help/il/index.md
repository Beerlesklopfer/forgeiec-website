---
title: "Instruction List Editor"
summary: "IL editor: accumulator-based IEC 61131-3 language with CR register"
---

## Overview

**Instruction List (IL)** is the assembler-like text language of
IEC 61131-3 and historically the first of the five IEC languages.
Programs are sequences of instructions that manipulate a single
internal **accumulator register** — the *Current Result* (`CR`). Each
line is a statement of the form

```
[Label:] Operator [Modifier] [Operand] (* Comment *)
```

and either reads from or writes to the accumulator or an external
variable.

In ForgeIEC IL is edited via the `FIlEditor` — layout and tooling are
analogous to the [ST editor](../st/).

## Editor layout

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (tree-sitter-instruction-list grammar) |
+----------------------------------------+
```

| Area | Content |
|---|---|
| **Variable table** (top) | Declarations with Name, Type, Initial value, Address, Comment — in sync with the `VAR ... END_VAR` block. |
| **Code area** (bottom) | IL source with tree-sitter highlighting (`tree-sitter-instruction-list` grammar). |
| **Search bar** (Ctrl-F / Ctrl-H) | Find-and-replace bar. |

Online mode and the inline-value overlay work identically to the ST
editor.

## Accumulator model

The accumulator (`CR`) holds the intermediate result of the running
evaluation. A typical sequence:

  1. `LD x` — load `x` into the accumulator (`CR := x`)
  2. `AND y` — combine the accumulator with `y` (`CR := CR AND y`)
  3. `ST z` — store the accumulator into `z` (`z := CR`)

That makes IL a **stack-free, single-register machine** — very close to
the microcontroller platforms that dominated when the language was
standardised in 1993.

## Key operators

| Group | Operators | Effect |
|---|---|---|
| **Load / Store** | `LD`, `LDN`, `ST`, `STN` | Set accumulator / store accumulator (`N` = negated) |
| **Set / Reset** | `S`, `R` | Set / reset bit (BOOL variable, when `CR` = TRUE) |
| **Bit logic** | `AND`, `OR`, `XOR`, `NOT` | Combine accumulator with operand |
| **Arithmetic** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` | Accumulator + operand → accumulator |
| **Comparison** | `GT`, `GE`, `EQ`, `NE`, `LE`, `LT` | Comparison result into `CR` |
| **Jump** | `JMP`, `JMPC`, `JMPCN` | Jump to label (`C` = when `CR` = TRUE) |
| **Call** | `CAL`, `CALC`, `CALCN` | Call function-block instance |
| **Return** | `RET`, `RETC`, `RETCN` | Leave POU |

## Modifiers

An operator can be refined via suffix modifiers:

| Modifier | Meaning |
|---|---|
| `N` | **Negation** of the operand (`LDN x` loads `NOT x`) |
| `C` | **Conditional** — perform only when `CR` = TRUE (`JMPC label`) |
| `(`...`)` | **Bracket modifier** — defer evaluation until `)` closes |

The bracket form enables compound expressions without intermediate
variables:

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## When to use IL instead of ST

ST is the default choice today. IL still makes sense when:

  - **Microcontroller performance** is decisive — IL maps 1:1 to machine
    instructions in most matiec back-ends, with no intermediate
    optimisation.
  - **Legacy systems** must be kept compatible (S5/S7 AWL-derived logic,
    older ABB / Beckhoff installed base).
  - **Very compact logic blocks** — interlocks, latches, edge conditions
    are often two lines shorter in IL than in ST.

For everything else, ST is more readable and easier to maintain.

## Code example — latching contactor with NO/NC contacts

Classic **contactor self-hold** in IL: pressing `start` energises
contactor `K1`, the `stop` button (NC, low-active) drops it again.
Logic:

```
K1 := (start OR K1) AND NOT stop
```

In IL:

```
PROGRAM Selbsthaltung
VAR
    start  AT %IX0.0 : BOOL;       (* NO push-button *)
    stop   AT %IX0.1 : BOOL;       (* NC push-button, low-active *)
    K1     AT %QX0.0 : BOOL;       (* contactor *)
END_VAR

    LD    start
    OR    K1                    (* CR := start OR K1 *)
    ANDN  stop                  (* CR := CR AND NOT stop *)
    ST    K1                    (* K1 := CR *)
END_PROGRAM
```

Four instructions, one register, no temporary storage. Exactly the kind
of construct IL was originally designed for.

## Related topics

- [Structured Text](../st/) — the Pascal-like sister language
- [Library](../library/) — function blocks callable via `CAL`
- [Project file format](../file-format/) — IL body inside `<body><IL>...`
