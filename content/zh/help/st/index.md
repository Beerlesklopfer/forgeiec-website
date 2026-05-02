---
title: "Structured Text 编辑器"
summary: "ST 编辑器 + 语言基础：IEC 61131-3 语句、位访问、限定池引用"
---

## 概述

**Structured Text (ST)** 是 IEC 61131-3 中类 Pascal 的高级语言，
也是 ForgeIEC 中 PROGRAM、FUNCTION_BLOCK 和 FUNCTION POU 的
默认编辑器。该编辑器是基于 `QWidget` 的组合，由变量表和代码区
通过垂直分割器耦合而成。

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

## 编辑器布局

| 区域 | 内容 |
|---|---|
| **变量表**（顶部） | 包含 Name、Type、Initial value、Address、Comment 列的声明。编辑会实时同步到代码的 `VAR ... END_VAR` 块。 |
| **代码区**（底部） | 变量段之间的 ST 源代码。基于 tree-sitter AST 的行折叠，行号，光标行高亮。 |
| **搜索栏**（Ctrl-F / Ctrl-H） | 显示在代码区上方，并带有用于查找替换的替换模式。 |

分割器在布局状态中按 POU 记忆其位置。

## Tree-sitter 语法高亮

ForgeIEC 不使用基于正则表达式的 `QSyntaxHighlighter`，而是用
**Tree-sitter** 把 ST 源解析为 AST 并通过捕获查询着色：

  - **关键字**（`IF`、`THEN`、`FOR`、`FUNCTION_BLOCK`、…）：洋红色
  - **数据类型**（`BOOL`、`INT`、`REAL`、`TIME`、…）：青色
  - **字符串 + 时间字面量**（`'abc'`、`T#20ms`）：绿色
  - **注释**（`(* ... *)`、`// ...`）：灰色，斜体
  - **PUBLISH / SUBSCRIBE**：Anvil 扩展关键字，专用样式

好处：在复杂结构（嵌套注释、时间字面量、限定引用）下高亮
仍然正确，且同一 AST 也驱动代码折叠所需的可折叠区间。

## 代码补全（Ctrl-Space）

按 **Ctrl-Space** 或键入两个匹配字符会打开补全弹窗。
补全器知道：

  - **IEC 关键字**（`IF`、`CASE`、`FOR`、`WHILE`、`RETURN`、…）
  - **数据类型**（`BOOL`、`INT`、`DINT`、`REAL`、`STRING`、`TIME`、…）
  - 当前 POU 的**局部变量**
  - 项目中的 **POU 名称**（PROGRAM、FUNCTION_BLOCK、FUNCTION）
  - **库块**（`TON`、`R_TRIG`、`JK_FF`、`DEBOUNCE`、…）
  - **标准函数**（`ABS`、`SQRT`、`LIMIT`、`LEN`、…）

变量池的变化（`poolChanged` 信号）以 100 ms 的去抖延迟传播
进补全模型 —— 新池条目几乎立即可用，无需每次按键都触发
完整重扫。

## 语言基础（IEC 61131-3）

### 语句

| 语句 | 形式 |
|---|---|
| **赋值** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | 离开循环 / 离开 POU |

### 表达式

具有 IEC 优先级的标准运算符：`**`、一元 `+/-/NOT`、`* / MOD`、
`+ -`、比较运算、`AND / &`、`XOR`、`OR`。括号用法与 Pascal 相同。
不允许隐式数值类型转换 —— 必须显式调用 `INT_TO_DINT`、
`REAL_TO_INT` 等。

### 对 ANY_BIT 类型的位访问

`var.<bit>` 直接在 `BYTE`/`WORD`/`DWORD`/`LWORD` 变量上
提取或置位单个位：

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

编译器将其翻译为干净的位掩码（`AND`/`OR`/移位），
不使用辅助变量。

### 三级限定引用

`<Category>.<Group>.<Variable>` 直接访问池条目，
无需显式声明 GVL：

| 前缀 | 来源 |
|---|---|
| `Anvil.X.Y`   | `anvilGroup="X"` 的池条目 |
| `Bellows.X.Y` | `hmiGroup="X"` 的池条目 |
| `GVL.X.Y`     | `gvlNamespace="X"` 的池条目 |
| `HMI.X.Y`     | `Bellows.X.Y` 的同义词 |

`Anvil.X.Y` 和 `Bellows.X.Y` 可独立指向不同的池条目 ——
只要 IEC 地址不同，编译器就会发出独立的 C 符号。

### 定位变量（`AT %...`）

定位变量将声明绑定到 IEC 地址：

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

地址是池中的主键 —— 详见
[项目文件格式](../file-format/)。

## 代码示例

### 示例 1 —— 使用库块进行 TON 调用

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

`fbDelay` 是库 FB `TON` 的实例。`start_button` 持续保持 3 秒后，
`motor_run` 切换为 TRUE。

### 示例 2 —— Bellows 读取驱动输出

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` 和 `Anvil.Sensors.contact_door` 是
编译器无需 GVL 声明即可解析的三级引用 —— 前提是两个标签
都保留在地址池中，且组 `Pfirsich` 的 HMI 导出已激活。

## 相关主题

- [库](../library/) —— 可用的功能块 + 函数
- [Instruction List](../il/) —— 替代的文本编辑器（基于累加器）
- [项目文件格式](../file-format/) —— ST 代码在 `.forge` 中的存储方式
