---
title: "Assignment & operator precedence"
summary: ":= is assignment (= is comparison). Precedence runs from parentheses (highest) down to OR (lowest); use parentheses when in doubt."
weight: 40
iec_chapter: "6.6.1"
construct_kind: "operator"
keywords: [":=", "assignment", "precedence", "associativity"]
llm_signals:
  - error_pattern: "Expected ':=' but found '='"
    where: "FStCompiler"
    diagnosis: "Assignment uses `:=` in IEC 61131-3, not `=`. The `=` token is the equality comparison operator. Languages where `=` is assignment (BASIC, Python) are the common porting source for this slip."
    fix_strategy: "Replace `=` with `:=` in assignment context."
    fix_example: |
      (* before — fails: Expected ':=' but found '=' *)
      iCount = iCount + 1;
      (* after *)
      iCount := iCount + 1;
  - error_pattern: "assignment to constant"
    where: "FStCompiler"
    diagnosis: "Trying to assign to a variable declared `VAR CONSTANT` or to a function input (`VAR_INPUT`) inside the function body."
    fix_strategy: "Either declare a separate non-const variable, or move the value through `VAR_OUTPUT` if the goal is to return something from the FB."
    fix_example: |
      (* before — fails *)
      VAR_INPUT iLimit : INT; END_VAR
      iLimit := iLimit + 1;
      (* after *)
      VAR_INPUT iLimit : INT; END_VAR
      VAR iWorkingLimit : INT; END_VAR
      iWorkingLimit := iLimit + 1;
  - error_pattern: "type mismatch in assignment"
    where: "matiec"
    diagnosis: "The right-hand side has a different type from the left-hand side and matiec won't auto-convert. Same root rule as the arithmetic-and-comparison type-strictness; just shows up at assignment time."
    fix_strategy: "Use the explicit conversion function: `INT_TO_REAL`, `BYTE_TO_INT`, `STRING_TO_INT`, etc."
    fix_example: |
      (* before — fails *)
      VAR iCount : INT; rTotal : REAL; END_VAR
      rTotal := iCount;
      (* after *)
      rTotal := INT_TO_REAL(iCount);
---

## Assignment

The assignment operator in IEC 61131-3 is **`:=`** (colon-equals).
This is one of the most frequent confusion points for
programmers coming from other languages:

| Language | Assignment | Equality |
|---|---|---|
| **IEC 61131-3 / Pascal** | `:=` | `=` |
| C / C++ / Java / JS | `=` | `==` |
| BASIC / Python | `=` | `==` (Py) / `=` (BASIC) |

Inside an IEC ST body:

```iec-st
iCount := iCount + 1;       (* assignment *)
IF iCount = 10 THEN ...     (* equality — comparison *)
```

`=` in an assignment context is a syntax error.

## Operator precedence (highest to lowest)

| Class | Operators | Associativity |
|---|---|---|
| Parentheses | `(...)` | n/a |
| Function call | `name(...)` | left |
| Component access | `.member`, `[index]`, `bit.N` | left |
| Exponent | `**` | **right** |
| Unary | `-` (negation), `NOT` | n/a |
| Multiplicative | `*`, `/`, `MOD` | left |
| Additive | `+`, `-` (binary) | left |
| Comparison | `<`, `<=`, `>`, `>=` | left |
| Equality | `=`, `<>` | left |
| Bitwise/Logical AND | `AND`, `&` | left |
| Bitwise/Logical XOR | `XOR` | left |
| Bitwise/Logical OR | `OR` | left |

`**` is the only right-associative operator: `2 ** 3 ** 2` is
`2 ** (3 ** 2) = 2 ** 9 = 512`, not `(2 ** 3) ** 2 = 64`.

## Precedence in practice

When in doubt, parenthesise. The IEC standard's precedence is
identical to most C-family languages **except** for the unified
binding of `AND` / `OR` / `XOR` (in C, `&&` and `||` bind
differently from `&` and `|`).

```iec-st
(* These two are equivalent — AND binds tighter than OR *)
xResult := xA OR xB AND xC;
xResult := xA OR (xB AND xC);

(* This is something else *)
xResult := (xA OR xB) AND xC;

(* Comparison binds tighter than equality, both bind tighter
   than AND/OR. So this works as expected: *)
xInRange := (iValue > 0) AND (iValue <= 100);

(* But the inner parens are STYLE, not necessary — a > b
   already returns BOOL before AND looks at it. *)
xInRange := iValue > 0 AND iValue <= 100;
```

## Multiple assignment

IEC 61131-3 third edition (2013) does **not** support
chained assignment in the C sense (`a = b = c = 0;`). Each
assignment is a separate statement:

```iec-st
(* not legal *)
(* iA := iB := iC := 0; *)

(* legal *)
iA := 0;
iB := 0;
iC := 0;
```

## IEC reference

- Assignment: clause **6.6.3.1** of IEC 61131-3 third edition
  (2013).
- Operator precedence: clause **6.6.1** Table 55.

## matiec conformance

matiec implements assignment and the precedence table per the
standard. The most common LLM mistakes (`=` instead of `:=`,
type-mismatch in assignment) are caught early by the local
FStCompiler — see the `llm_signals` block above for the
canonical fix patterns.
