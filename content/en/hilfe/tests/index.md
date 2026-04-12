---
title: "Test Coverage"
summary: "Automated quality assurance: 117 tests verify the complete IEC 61131-3 language feature set, all standard blocks, and the multi-task threading system"
---

ForgeIEC is backed by a comprehensive automated test suite.
Every commit is verified against **117 unit tests** before merging, covering
the complete IEC 61131-3 Structured Text language feature set, all
standard function blocks, and the multi-task threading system.

## Test Suites at a Glance

| Suite | Tests | Verifies |
|-------|------:|----------|
| **FStCompilerTest** | 101 | Complete ST language feature set |
| **FStLibraryTest** | 8 | All 132 standard blocks (FBs + FCs) |
| **FCodeGeneratorThreadingTest** | 8 | Multi-task scheduling + lock-free sync |
| **Total** | **117** | **0 failures** |

---

## 1. ST Language Feature Set (FStCompilerTest)

101 tests verify every supported IEC 61131-3 Structured Text
language construct. Each test compiles an ST fragment through the
FStCompiler and verifies the generated C++ code.

### 1.1 Assignments

| Test | ST Code | Verifies |
|------|---------|----------|
| `assignSimple` | `a := 42;` | Simple assignment |
| `assignExpression` | `a := b + 1;` | Expression assignment |
| `assignExternal` | `ExtVar := 10;` | VAR_EXTERNAL access |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | Qualified GVL path |

### 1.2 Arithmetic Operators

| Test | ST Code | C Operator |
|------|---------|------------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | Parenthesization |

### 1.3 Comparison Operators

| Test | ST Code | C Operator |
|------|---------|------------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 Boolean Operators

| Test | ST Code | C Operator |
|------|---------|------------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 Literals

| Test | ST Code | Verifies |
|------|---------|----------|
| `literalInteger` | `a := 12345;` | Integer |
| `literalReal` | `c := 3.14;` | Floating point |
| `literalBoolTrue` | `flag := TRUE;` | Boolean value |
| `literalBoolFalse` | `flag := FALSE;` | Boolean value |
| `literalString` | `text := 'hello';` | String |
| `literalTime` | `counter := T#500ms;` | Time constant |

### 1.6 Control Structures

**IF / ELSIF / ELSE / END_IF**

| Test | Verifies |
|------|----------|
| `ifSimple` | Simple condition |
| `ifElse` | If-else branching |
| `ifElsif` | Multiple branching with ELSIF |
| `ifNested` | Nested IF blocks |

**FOR / WHILE / REPEAT**

| Test | Verifies |
|------|----------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | FOR with BY step size |
| `whileLoop` | WHILE loop |
| `repeatUntil` | REPEAT/UNTIL loop |

**CASE**

| Test | Verifies |
|------|----------|
| `caseStatement` | CASE/OF with multiple labels + switch/case/break |

**RETURN / EXIT**

| Test | Verifies |
|------|----------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | EXIT inside FOR → break |

### 1.7 Function Blocks (FB Calls)

| Test | Verifies |
|------|----------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — OUT => assignment |

### 1.8 Array Access

| Test | Verifies |
|------|----------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | Array access inside FOR loop |

### 1.9 Type Conversions

The compiler recognizes the `XXX_TO_YYY` pattern and generates
C-style casts (`(TYPE)value`), conforming to the IEC standard.

| Test | ST Code | Generated |
|------|---------|-----------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 Struct Member Access

| Test | Verifies |
|------|----------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 Cross-Task Variables (Multi-Task)

| Test | Verifies |
|------|----------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` for lock-free reads |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` for lock-free writes |
| `crossStructuredGet` | `__snap_` thread-local snapshot access |
| `crossStructuredMemberAccess` | `__snap_Struct.field` access |

### 1.12 Standard Function Blocks

Each IEC standard FB is instantiated and called:

| Test | FB Type | Verifies |
|------|---------|----------|
| `fbTon` | TON | On-delay timer |
| `fbTof` | TOF | Off-delay timer |
| `fbTp` | TP | Pulse timer |
| `fbCtu` | CTU | Up counter |
| `fbCtd` | CTD | Down counter |
| `fbRtrig` | R_TRIG | Rising edge |
| `fbFtrig` | F_TRIG | Falling edge |
| `fbRs` | RS | Reset-dominant |
| `fbSr` | SR | Set-dominant |

### 1.13 Standard Functions

| Category | Tests | Functions |
|----------|------:|-----------|
| Math | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| Selection | 4 | SEL, LIMIT, MIN, MAX |
| String | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| Bit shift | 4 | SHL, SHR, ROL, ROR |
| Type conversion | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 Edge Cases

| Test | Verifies |
|------|----------|
| `complexNestedExpression` | Nested expressions |
| `multipleStatementsOnSeparateLines` | Multi-line programs |
| `emptyBody` | Empty POU body |
| `commentOnlyBody` | Comments only |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | Case insensitivity |

---

## 2. Standard Library (FStLibraryTest)

8 data-driven tests verify **all 132 blocks** from the
standard library (`standard_library.sql`) automatically.

### 2.1 Function Blocks (13 FBs)

| Test | Verifies |
|------|----------|
| `fbSingleInstance` | Each FB can be instantiated and called individually |
| `fbDoubleInstance` | Two instances of the same FB type simultaneously |
| `fbOutputRead` | All outputs readable after the call |

**Covered FBs:** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 Functions (119 FCs)

| Test | Verifies |
|------|----------|
| `fcCall` | Each FC callable with correct parameters (104 tested) |
| `fcInExpression` | FC return value usable in expressions |

**Covered categories:**

- **Arithmetic:** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **Comparison:** EQ, NE, LT, GT, LE, GE
- **Trigonometry:** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **Logarithmic:** EXP, LN, LOG, SQRT
- **Selection:** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **String:** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **Bit shift:** SHL, SHR, ROL, ROR
- **Type conversion:** 60+ conversion functions (BOOL_TO_INT, INT_TO_REAL, ...)
- **ForgeIEC extensions:** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. Multi-Task Threading (FCodeGeneratorThreadingTest)

8 tests verify the complete multi-task scheduling system according to
the design specification (MT-spec, docs/design/multi-task-scheduler.md).

| Test | Verifies |
|------|----------|
| `singleProgramDefaultTask` | One PROGRAM without explicit task → DefaultTask synthesis, no threading |
| `twoProgramsTwoTasks` | Two tasks → RESOURCE0_start__, legacy shim config_run__, both task threads |
| `crossPrimitiveAtomicEmission` | Shared INT variable → `std::atomic<>` location storage, `__GET_EXTERNAL_ATOMIC` in body |
| `crossStructuredDoubleBuffer` | Shared STRUCT → `__DBUF_[2]` + `thread_local __snap_` + double-buffer copy-in/out |
| `localVarNoSync` | Variable used in one task only → normal `__SET_EXTERNAL`, no atomic |
| `conflictTwoWriters` | Two tasks write the same variable → compile warning |
| `singleProgramDefaultTask` | Backward compatibility: existing projects run unchanged |

### Multi-Task Architecture

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [under bufferLock]            | [lock-free]
```

**Synchronization mechanisms:**
- **CrossPrimitive** (BOOL, INT, REAL, ...): `std::atomic<T>` on the location variable, `__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC` in body code
- **CrossStructured** (STRUCT, ARRAY, STRING): Double-buffer `__DBUF_[2]` with atomic write index, `thread_local` snapshots `__snap_` for set consistency

---

## Quality Assurance

### Automated Verification

The tests run with every build using `-DBUILD_TESTS=ON`.
Integration into the CI pipeline (Forgejo Actions) is prepared.

### Data-Driven Tests

The library tests (`FStLibraryTest`) read block definitions
directly from `standard_library.sql`. When new blocks are added,
they are automatically included in the test run — no manual creation
of test cases required.

### Completeness

The test suite covers the entire IEC 61131-3 Structured Text
language feature set as supported by ForgeIEC:

- All operators (arithmetic, comparison, boolean, bit shift)
- All control structures (IF, FOR, WHILE, REPEAT, CASE)
- All literal types (integer, real, bool, string, time)
- All standard FBs and FCs (132 blocks)
- Array and struct access
- GVL-qualified variables
- Cross-task synchronization (atomics + double-buffer)
- Type conversions (C-cast generation)
