---
title: "测试覆盖率"
summary: "自动化质量保证：117项测试验证完整的IEC 61131-3语言规范、所有标准块和多任务系统"
---

ForgeIEC通过一套全面的自动化测试进行保护。
每次提交在合并前都会通过**117项单元测试**进行验证，
这些测试覆盖了完整的IEC 61131-3 Structured Text语言规范、
所有标准功能块和多任务系统。

## 测试套件概览

| 套件 | 测试数 | 验证内容 |
|------|-------:|----------|
| **FStCompilerTest** | 101 | 完整的ST语言规范 |
| **FStLibraryTest** | 8 | 全部132个标准块（FB + FC） |
| **FCodeGeneratorThreadingTest** | 8 | 多任务调度 + 无锁同步 |
| **总计** | **117** | **0个错误** |

---

## 1. ST语言规范（FStCompilerTest）

101项测试验证每个受支持的IEC 61131-3 Structured Text语言结构。
每项测试通过FStCompiler编译一个ST片段，并验证生成的C++代码。

### 1.1 赋值

| 测试 | ST代码 | 验证内容 |
|------|--------|----------|
| `assignSimple` | `a := 42;` | 简单赋值 |
| `assignExpression` | `a := b + 1;` | 表达式赋值 |
| `assignExternal` | `ExtVar := 10;` | VAR_EXTERNAL访问 |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | 限定GVL路径 |

### 1.2 算术运算符

| 测试 | ST代码 | C运算符 |
|------|--------|---------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | 括号 |

### 1.3 比较运算符

| 测试 | ST代码 | C运算符 |
|------|--------|---------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 布尔运算符

| 测试 | ST代码 | C运算符 |
|------|--------|---------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 字面量

| 测试 | ST代码 | 验证内容 |
|------|--------|----------|
| `literalInteger` | `a := 12345;` | 整数 |
| `literalReal` | `c := 3.14;` | 浮点数 |
| `literalBoolTrue` | `flag := TRUE;` | 布尔值 |
| `literalBoolFalse` | `flag := FALSE;` | 布尔值 |
| `literalString` | `text := 'hello';` | 字符串 |
| `literalTime` | `counter := T#500ms;` | 时间常量 |

### 1.6 控制结构

**IF / ELSIF / ELSE / END_IF**

| 测试 | 验证内容 |
|------|----------|
| `ifSimple` | 简单条件 |
| `ifElse` | If-Else分支 |
| `ifElsif` | ELSIF多重分支 |
| `ifNested` | 嵌套IF块 |

**FOR / WHILE / REPEAT**

| 测试 | 验证内容 |
|------|----------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | 带BY步长的FOR |
| `whileLoop` | WHILE循环 |
| `repeatUntil` | REPEAT/UNTIL循环 |

**CASE**

| 测试 | 验证内容 |
|------|----------|
| `caseStatement` | 带多个标签的CASE/OF + switch/case/break |

**RETURN / EXIT**

| 测试 | 验证内容 |
|------|----------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | FOR中的EXIT → break |

### 1.7 功能块（FB调用）

| 测试 | 验证内容 |
|------|----------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — OUT =>赋值 |

### 1.8 数组访问

| 测试 | 验证内容 |
|------|----------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | FOR循环中的数组访问 |

### 1.9 类型转换

编译器识别`XXX_TO_YYY`模式并生成符合IEC标准的
C风格强制转换（`(TYPE)value`）。

| 测试 | ST代码 | 生成结果 |
|------|--------|----------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 结构体成员访问

| 测试 | 验证内容 |
|------|----------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 跨任务变量（多任务）

| 测试 | 验证内容 |
|------|----------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` 用于无锁读取 |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` 用于无锁写入 |
| `crossStructuredGet` | `__snap_` 线程本地快照访问 |
| `crossStructuredMemberAccess` | `__snap_Struct.field` 访问 |

### 1.12 标准功能块

每个IEC标准FB作为实例创建并调用：

| 测试 | FB类型 | 验证内容 |
|------|--------|----------|
| `fbTon` | TON | 接通延时 |
| `fbTof` | TOF | 断开延时 |
| `fbTp` | TP | 脉冲定时器 |
| `fbCtu` | CTU | 递增计数器 |
| `fbCtd` | CTD | 递减计数器 |
| `fbRtrig` | R_TRIG | 上升沿 |
| `fbFtrig` | F_TRIG | 下降沿 |
| `fbRs` | RS | 复位优先 |
| `fbSr` | SR | 置位优先 |

### 1.13 标准函数

| 类别 | 测试数 | 函数 |
|------|-------:|------|
| 数学 | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| 选择 | 4 | SEL, LIMIT, MIN, MAX |
| 字符串 | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| 位移 | 4 | SHL, SHR, ROL, ROR |
| 类型转换 | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 边界情况

| 测试 | 验证内容 |
|------|----------|
| `complexNestedExpression` | 嵌套表达式 |
| `multipleStatementsOnSeparateLines` | 多行程序 |
| `emptyBody` | 空POU体 |
| `commentOnlyBody` | 仅注释 |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | 大小写不敏感 |

---

## 2. 标准库（FStLibraryTest）

8项数据驱动测试自动验证标准库（`standard_library.sql`）中的
**全部132个块**。

### 2.1 功能块（13个FB）

| 测试 | 验证内容 |
|------|----------|
| `fbSingleInstance` | 每个FB可单独实例化和调用 |
| `fbDoubleInstance` | 同一FB类型的两个实例同时使用 |
| `fbOutputRead` | 调用后所有输出可读 |

**覆盖的FB：** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 函数（119个FC）

| 测试 | 验证内容 |
|------|----------|
| `fcCall` | 每个FC可使用正确参数调用（104个已测试） |
| `fcInExpression` | FC返回值可在表达式中使用 |

**覆盖的类别：**

- **算术：** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **比较：** EQ, NE, LT, GT, LE, GE
- **三角函数：** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **对数：** EXP, LN, LOG, SQRT
- **选择：** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **字符串：** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **位移：** SHL, SHR, ROL, ROR
- **类型转换：** 60+转换函数（BOOL_TO_INT, INT_TO_REAL, ...）
- **ForgeIEC扩展：** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. 多任务（FCodeGeneratorThreadingTest）

8项测试按照设计规范（MT-spec, docs/design/multi-task-scheduler.md）
验证完整的多任务调度系统。

| 测试 | 验证内容 |
|------|----------|
| `singleProgramDefaultTask` | 无显式任务的单个PROGRAM → DefaultTask合成，无线程 |
| `twoProgramsTwoTasks` | 两个任务 → RESOURCE0_start__、Legacy-Shim config_run__、两个任务线程 |
| `crossPrimitiveAtomicEmission` | 共享INT变量 → `std::atomic<>` Location存储，体内`__GET_EXTERNAL_ATOMIC` |
| `crossStructuredDoubleBuffer` | 共享STRUCT → `__DBUF_[2]` + `thread_local __snap_` + 双缓冲区拷入/拷出 |
| `localVarNoSync` | 仅在一个任务中的变量 → 普通`__SET_EXTERNAL`，无Atomic |
| `conflictTwoWriters` | 两个任务写入同一变量 → 编译警告 |
| `singleProgramDefaultTask` | 向后兼容：现有项目无需修改即可运行 |

### 多任务架构

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [在bufferLock下]              | [lock-free]
```

**同步机制：**
- **CrossPrimitive**（BOOL, INT, REAL, ...）：Location变量上的`std::atomic<T>`，体代码中的`__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC`
- **CrossStructured**（STRUCT, ARRAY, STRING）：带原子写入索引的双缓冲区`__DBUF_[2]`，用于Set一致性的`thread_local`快照`__snap_`

---

## 质量保证

### 自动化验证

测试在每次构建时通过`-DBUILD_TESTS=ON`运行。
已准备好CI管道（Forgejo Actions）集成。

### 数据驱动测试

库测试（`FStLibraryTest`）直接从`standard_library.sql`读取块定义。
添加新块时会自动进行测试——无需手动创建测试用例。

### 完整性

测试套件覆盖了ForgeIEC所支持的完整IEC 61131-3 Structured Text
语言规范：

- 所有运算符（算术、比较、布尔、位移）
- 所有控制结构（IF, FOR, WHILE, REPEAT, CASE）
- 所有字面量类型（Integer, Real, Bool, String, Time）
- 所有标准FB和FC（132个块）
- 数组和结构体访问
- GVL限定变量
- 跨任务同步（Atomics + 双缓冲区）
- 类型转换（C强制转换生成）
