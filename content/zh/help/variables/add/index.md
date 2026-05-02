---
title: "添加变量"
summary: "FAddVariableDialog —— 在一个模态窗口中收集所有字段，支持批量创建的范围模式以及数组包装器"
---

## 概述

**FAddVariableDialog** 是用于向 POU 或池中添加新变量的
模态窗口。它在一个步骤内收集所有字段，并在表单下方
显示生成的 IEC ST 声明的**实时预览** —— 您输入的内容会
立即渲染为完整的 `VAR ... END_VAR` 片段。

对话框以两种模式运行：

  - **添加模式**：字段为空，OK 创建新变量。可通过变量
    面板中的加号图标或 POU 编辑器中的 Ctrl+N 触发。
  - **编辑模式**：双击面板中已有的变量 —— 使用相同的
    对话框，每个字段都已预填充。

## 字段

| 字段 | 必填 | 含义 |
|---|---|---|
| **Name** | 是 | 程序员可见的名称。按 IEC 标识符规则（字母 + 字母/数字/`_`）校验。可结合范围模式用于批量创建（见下文）。 |
| **Type** | 是 | 包含 IEC 基本类型、标准 FB、项目 FB、用户自定义数据类型的下拉框。数组创建由包装器复选框处理。 |
| **Direction** | 取决于 POU | 变量类别 —— 见下文。 |
| **Initial** | 否 | 初始值（`FALSE`、`0`、`T#100ms`、`'OFF'`）。 |
| **Address** | 否 | 仅对 VarList POU 使用。为空 = 创建时由 `pool->nextFreeAddress` 自动分配。 |
| **Retain** | 否 | 复选框 —— RETAIN，掉电后值保留。 |
| **Constant** | 否 | 复选框 —— `VAR CONSTANT`，运行时不可写入。 |
| **Array wrapper** | 否 | 将所选类型包装为 `ARRAY [..] OF`。 |
| **Documentation** | 否 | 自由文本注释，作为 `<documentation>` 存储于 PLCopen XML 中。 |

## 用于批量创建的范围模式

无需逐个输入 `LED_0`、`LED_1`、… `LED_7`，您可以在名称
字段中指定一个**范围模式**：

| 输入 | 效果 |
|---|---|
| `LED_0..7` | 创建八个变量 `LED_0` 到 `LED_7`。 |
| `LED_0-7` | 同义，效果相同。 |
| `Sensor_1..3` | 创建三个变量 `Sensor_1` 到 `Sensor_3`。 |

每次批量创建时，如果地址已设置则会递增：
`%QX0.0` → `%QX0.0`、`%QX0.1`、…、`%QX0.7`。

## 数组包装器复选框

如果要把**一个**变量声明为数组，请勾选数组复选框。
将出现两个用于索引范围的微调框，类型在运行时被
包装为 `ARRAY [..] OF <type>`。

| 类型下拉 | 数组复选框 | 索引范围 | 生成的声明 |
|---|---|---|---|
| `INT` | 关 | — | `: INT;` |
| `INT` | 开 | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | 开 | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor`（用户结构体） | 开 | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

包装器特意放在复选框上而非类型下拉中 —— 这样保持
下拉简洁，并允许构建任何类型的数组而无需在下拉中查找。

## 类型下拉

下拉将四个来源汇总为一个列表：

  1. **IEC 基本类型**：`BOOL`、`BYTE`、`WORD`、`DWORD`、`LWORD`、
     `INT`、`DINT`、`LINT`、`UINT`、`UDINT`、`ULINT`、`REAL`、`LREAL`、
     `TIME`、`DATE`、`TIME_OF_DAY`、`DATE_AND_TIME`、`STRING`、`WSTRING`。
  2. 来自库的**标准 FB**：`TON`、`TOF`、`TP`、`R_TRIG`、
     `F_TRIG`、`CTU`、`CTD`、`CTUD`、`SR`、`RS`、…
  3. **项目功能块** —— 当前项目中声明的每个 FB
     （用户库）。
  4. 来自 `<dataTypes>` 的**用户自定义数据类型**：STRUCT、枚举、别名。

ARRAY 模板**不**出现在下拉中 —— 它们通过包装器复选框处理。

## 各 POU 类型的方向（变量类别）

可用的方向值取决于 POU 类型：

| POU 类型 | 可用方向 |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | 固定为 `VAR_GLOBAL` —— 下拉隐藏。 |
| `AnvilVarList` | 固定为 `VAR_GLOBAL`（自动生成）—— 下拉隐藏。 |
| 池全局变量（无 POU 容器） | 无方向 —— `%I`/`%Q` 地址隐式确定。 |

## 编辑模式

双击变量面板中已有的变量会打开同一个对话框。
每个字段均已预填充；OK 时变更通过 `pou->renameVariable` /
`pool->rebind` 路由（以保持 `byAddress` 索引同步）。
对话框通过 `existing != nullptr` 检测编辑模式。

## 示例 —— 一次创建 8 个 LED

将 8 个输出 LED 作为池变量在一个步骤中创建：

  - **Name**：`LED_0..7`
  - **Type**：`BOOL`
  - **Direction**：隐藏（池全局）
  - **Address**：`%QX0.0`（自动递增）
  - **Initial**：`FALSE`

OK 创建八个池条目：

```text
LED_0  AT %QX0.0 : BOOL := FALSE;
LED_1  AT %QX0.1 : BOOL := FALSE;
LED_2  AT %QX0.2 : BOOL := FALSE;
LED_3  AT %QX0.3 : BOOL := FALSE;
LED_4  AT %QX0.4 : BOOL := FALSE;
LED_5  AT %QX0.5 : BOOL := FALSE;
LED_6  AT %QX0.6 : BOOL := FALSE;
LED_7  AT %QX0.7 : BOOL := FALSE;
```

随后可在变量面板中选中这八个变量，并通过批量操作
分配到一个 HMI 组 —— 例如 `Set HMI Group... -> Frontpanel`。

## 相关主题

  - [变量管理](../) —— 包含列、过滤器和批量操作的
    变量面板。
  - [项目文件格式](../../file-format/) —— 池在 PLCopen XML 中
    如何作为 `<addData>` 块持久化。
