---
title: "Structured Text Editor"
summary: "ST editor + language fundamentals: IEC 61131-3 statements, bit access, qualified pool references"
---

## Overview

**Structured Text (ST)** is the Pascal-like high-level language of
IEC 61131-3 and the default editor for PROGRAM, FUNCTION_BLOCK, and
FUNCTION POUs in ForgeIEC. The editor is a `QWidget`-based composition
of a variable table and a code area, coupled through a vertical splitter.

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT/VAR_INST)    |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (Tree-sitter highlighting + folding +  |
|  Ctrl-Space completion)                |
+----------------------------------------+
```

## Editor layout

| Area | Content |
|---|---|
| **Variable table** (top) | Declarations with columns Name, Type, Initial value, Address, Comment. Edits sync live into the `VAR ... END_VAR` block of the code. |
| **Code area** (bottom) | ST source between the variable sections. Line folding driven by the tree-sitter AST, line numbers, cursor-line highlight. |
| **Search bar** (Ctrl-F / Ctrl-H) | Shown above the code area, with replace mode for find-and-replace. |

The splitter remembers its position per POU in the layout state.

## Tree-sitter syntax highlighting

Instead of a regex-based `QSyntaxHighlighter`, ForgeIEC parses ST source
with **Tree-sitter** into an AST and colours via capture queries:

  - **Keywords** (`IF`, `THEN`, `FOR`, `FUNCTION_BLOCK`, ...): magenta
  - **Data types** (`BOOL`, `INT`, `REAL`, `TIME`, ...): cyan
  - **Strings + time literals** (`'abc'`, `T#20ms`): green
  - **Comments** (`(* ... *)`, `// ...`): grey, italic
  - **PUBLISH / SUBSCRIBE**: Anvil extension keywords, dedicated style

Benefit: highlighting stays correct on complex constructs (nested
comments, time literals, qualified references), and the same AST drives
the foldable ranges for code folding.

## Code completion (Ctrl-Space)

Pressing **Ctrl-Space** or typing two matching characters opens the
completion popup. The completer knows:

  - **IEC keywords** (`IF`, `CASE`, `FOR`, `WHILE`, `RETURN`, ...)
  - **Data types** (`BOOL`, `INT`, `DINT`, `REAL`, `STRING`, `TIME`, ...)
  - **Local variables** of the current POU
  - **POU names** in the project (PROGRAM, FUNCTION_BLOCK, FUNCTION)
  - **Library blocks** (`TON`, `R_TRIG`, `JK_FF`, `DEBOUNCE`, ...)
  - **Standard functions** (`ABS`, `SQRT`, `LIMIT`, `LEN`, ...)

Changes to the variable pool (`poolChanged` signal) propagate into the
completion model with 100 ms debounce — new pool entries become
available almost instantly, without every keystroke triggering a full
rescan.

## Language fundamentals (IEC 61131-3)

### Statements

| Statement | Form |
|---|---|
| **Assignment** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | Leave loop / leave POU |

### Expressions

Standard operators with IEC precedence: `**`, unary `+/-/NOT`, `* / MOD`,
`+ -`, comparisons, `AND / &`, `XOR`, `OR`. Parentheses as in Pascal.
Implicit numeric type conversions are not allowed — `INT_TO_DINT`,
`REAL_TO_INT` etc. must be called explicitly.

### Bit access on ANY_BIT types

`var.<bit>` extracts or sets a single bit, directly on
`BYTE`/`WORD`/`DWORD`/`LWORD` variables:

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

The compiler translates this into clean bit masking with `AND`/`OR`/shift,
without helper variables.

### 3-level qualified references

`<Category>.<Group>.<Variable>` accesses pool entries directly, without
having to declare GVLs explicitly:

| Prefix | Source |
|---|---|
| `Anvil.X.Y`   | Pool entry with `anvilGroup="X"` |
| `Bellows.X.Y` | Pool entry with `hmiGroup="X"` |
| `GVL.X.Y`     | Pool entry with `gvlNamespace="X"` |
| `HMI.X.Y`     | Synonym for `Bellows.X.Y` |

`Anvil.X.Y` and `Bellows.X.Y` may independently point to different pool
entries — the compiler emits separate C symbols as soon as the IEC
addresses differ.

### Located variables (`AT %...`)

Located variables bind a declaration to an IEC address:

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

Address is the primary key in the pool — see
[Project file format](../file-format/).

## Code examples

### Example 1 — TON call with library block

```text
PROGRAM PLC_PRG
VAR
    start_button   AT %IX0.0  : BOOL;
    motor_run      AT %QX0.0  : BOOL;
    fbDelay        : TON;
END_VAR

fbDelay(IN := start_button, PT := T#3s);
motor_run := fbDelay.Q;
END_PROGRAM
```

`fbDelay` is an instance of the library FB `TON`. After 3 seconds of
held `start_button`, `motor_run` switches to TRUE.

### Example 2 — Bellows read driving an output

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` and `Anvil.Sensors.contact_door` are 3-level
references the compiler resolves without a GVL declaration — provided
both tags are kept in the address pool and the HMI export for the
group `Pfirsich` is active.

## Related topics

- [Library](../library/) — available function blocks + functions
- [Instruction List](../il/) — alternative text editor (accumulator-based)
- [Project file format](../file-format/) — how ST code is stored in `.forge`
