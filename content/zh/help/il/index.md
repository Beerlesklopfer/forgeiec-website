---
title: "Instruction List 编辑器"
summary: "IL 编辑器：基于累加器的 IEC 61131-3 语言，使用 CR 寄存器"
---

## 概述

**Instruction List (IL)** 是 IEC 61131-3 中类汇编的文本语言，
也是历史上 IEC 五种语言中的第一个。
程序是一系列操作内部单一**累加器寄存器** ——
即*当前结果*（`CR`）—— 的指令。每行都是如下形式的语句：

```
[Label:] Operator [Modifier] [Operand] (* Comment *)
```

每行要么从累加器或外部变量读取，要么向其写入。

在 ForgeIEC 中 IL 通过 `FIlEditor` 编辑 —— 布局和工具与
[ST 编辑器](../st/)类似。

## 编辑器布局

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (tree-sitter-instruction-list grammar) |
+----------------------------------------+
```

| 区域 | 内容 |
|---|---|
| **变量表**（顶部） | 包含 Name、Type、Initial value、Address、Comment 的声明 —— 与 `VAR ... END_VAR` 块同步。 |
| **代码区**（底部） | 带 tree-sitter 高亮（`tree-sitter-instruction-list` 语法）的 IL 源代码。 |
| **搜索栏**（Ctrl-F / Ctrl-H） | 查找替换栏。 |

在线模式和内联值覆盖与 ST 编辑器工作方式相同。

## 累加器模型

累加器（`CR`）保存正在进行的求值的中间结果。典型序列：

  1. `LD x` —— 把 `x` 装入累加器（`CR := x`）
  2. `AND y` —— 累加器与 `y` 相组合（`CR := CR AND y`）
  3. `ST z` —— 把累加器存入 `z`（`z := CR`）

这使得 IL 成为**无栈的单寄存器机器** —— 非常贴近该语言
1993 年标准化时占主导地位的微控制器平台。

## 关键运算符

| 分组 | 运算符 | 效果 |
|---|---|---|
| **Load / Store** | `LD`、`LDN`、`ST`、`STN` | 设置累加器 / 存储累加器（`N` = 取反） |
| **Set / Reset** | `S`、`R` | 置位 / 复位（当 `CR` = TRUE 时对 BOOL 变量操作） |
| **位逻辑** | `AND`、`OR`、`XOR`、`NOT` | 累加器与操作数组合 |
| **算术** | `ADD`、`SUB`、`MUL`、`DIV`、`MOD` | 累加器 + 操作数 → 累加器 |
| **比较** | `GT`、`GE`、`EQ`、`NE`、`LE`、`LT` | 比较结果存入 `CR` |
| **跳转** | `JMP`、`JMPC`、`JMPCN` | 跳到标签（`C` = 当 `CR` = TRUE 时） |
| **调用** | `CAL`、`CALC`、`CALCN` | 调用功能块实例 |
| **返回** | `RET`、`RETC`、`RETCN` | 离开 POU |

## 修饰符

可通过后缀修饰符细化运算符：

| 修饰符 | 含义 |
|---|---|
| `N` | 操作数**取反**（`LDN x` 装入 `NOT x`） |
| `C` | **条件** —— 仅当 `CR` = TRUE 时执行（`JMPC label`） |
| `(`...`)` | **括号修饰符** —— 推迟求值直到 `)` 关闭 |

括号形式可在不使用中间变量的情况下实现复合表达式：

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## 何时使用 IL 而非 ST

如今 ST 是默认选择。在以下场景下 IL 仍有意义：

  - **微控制器性能**至关重要 —— 在大多数 matiec 后端中
    IL 与机器指令一一对应，没有中间优化。
  - 必须保持兼容的**遗留系统**（源自 S5/S7 AWL 的逻辑、
    较旧的 ABB / Beckhoff 装机基础）。
  - **非常紧凑的逻辑块** —— 互锁、自保持、边沿条件
    在 IL 中往往比 ST 短两行。

对于其他所有情况，ST 更易读、更易维护。

## 代码示例 —— 使用 NO/NC 触点的自保持接触器

经典的 IL 写法的**接触器自保持**：按下 `start` 使接触器
`K1` 通电，`stop` 按钮（NC，低有效）将其释放。
逻辑：

```
K1 := (start OR K1) AND NOT stop
```

IL 写法：

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

四条指令、一个寄存器、无临时存储。正是 IL 最初设计要解决的
那种结构。

## 相关主题

- [Structured Text](../st/) —— 类 Pascal 的姊妹语言
- [库](../library/) —— 可通过 `CAL` 调用的功能块
- [项目文件格式](../file-format/) —— `<body><IL>...` 中的 IL 主体
