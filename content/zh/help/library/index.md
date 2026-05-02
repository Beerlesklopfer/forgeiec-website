---
title: "库（功能块 + 函数）"
summary: "IEC 61131-3 标准库 + ForgeIEC 扩展 + 用户自定义块"
---

## 概述

ForgeIEC 库是应用程序可从 `.forge` 项目中调用的所有可重用构建
块的中央集合 —— 涵盖 IEC 61131-3 标准化的功能块与函数，以及项目
特定或 ForgeIEC 特有的扩展。

库显示在 **库面板**中（默认停靠位置：右侧边栏）。当库面板获得焦点时，
按 **F1** 即可打开此页面。

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (project-specific blocks)
```

库目前提供**近 100 个块**和**略多于 30 个函数**。每个条目包含：

  - **名称**（例如 `TON`、`JK_FF`）
  - **引脚列表**（输入与输出，包含类型和位置）
  - **类型**（带状态的 `FUNCTION_BLOCK` 或无状态的 `FUNCTION`）
  - **说明** + **帮助文本**及使用注意事项
  - **代码示例**（在库帮助面板中可见）

## 类别树

### 标准功能块

| 分组 | 块 |
|---|---|
| **双稳态** | `SR`、`RS` —— 带优先级的置位/复位 |
| **边沿检测** | `R_TRIG`、`F_TRIG` —— 上升沿/下降沿 |
| **计数器** | `CTU`、`CTD`、`CTUD` —— 加计数 / 减计数 / 双向计数 |
| **定时器** | `TON`、`TOF`、`TP` —— 接通延时 / 断开延时 / 脉冲 |
| **运动控制** | 速度曲线、斜坡、轨迹（开发中） |
| **信号生成** | 用于测试与验证信号的发生器 FB |
| **函数操纵器** | 保持、锁存、历史 |
| **闭环控制** | PID、滞环、双位控制 |
| **应用** *(ForgeIEC)* | `JK_FF`、`DEBOUNCE` —— 在实践中证明普遍有用的应用相关块 |

### 标准函数

| 分组 | 内容 |
|---|---|
| **算术运算** | `ADD`、`SUB`、`MUL`、`DIV`、`MOD`（适用于任何 ANY_NUM 类型） |
| **比较运算** | `EQ`、`NE`、`LT`、`LE`、`GT`、`GE` |
| **位运算** | `AND`、`OR`、`XOR`、`NOT`（适用于 ANY_BIT —— 详见 `help/st`） |
| **位移** | `SHL`、`SHR`、`ROL`、`ROR` |
| **选择** | `SEL`、`MAX`、`MIN`、`LIMIT`、`MUX` |
| **数学函数** | `ABS`、`SQRT`、`LN`、`LOG`、`EXP`、`SIN`、`COS`、`TAN`、`ASIN`、`ACOS`、`ATAN` |
| **字符串** | `LEN`、`LEFT`、`RIGHT`、`MID`、`CONCAT`、`INSERT`、`DELETE`、`REPLACE`、`FIND` |
| **类型转换** | `BOOL_TO_INT`、`REAL_TO_DINT`、`STRING_TO_INT`、… |

### 用户库

项目定义的功能块和函数 —— 任何声明为 `FUNCTION_BLOCK` 或
`FUNCTION` 的内容都会自动出现在此类别下，并可与标准块一样从项目的
任何位置调用。

## 库面板 —— 用法

| 操作 | 效果 |
|---|---|
| **搜索**（顶部放大镜） | 按块名称过滤树形视图 —— 输入 `to` 可找到 `TON`。 |
| **双击**某个块 | 在详细窗格中打开该块的帮助：引脚说明 + 代码示例。 |
| **拖动**到 ST 编辑器 | 在光标位置插入块调用，并在本地 `VAR_INST` 段中插入实例声明。 |
| **右键 > "Insert Call..."** | 与拖动相同，通过上下文菜单触发。 |
| 在某个块上按 **F1** | 打开此页面。 |

## 示例 1 —— 使用 `DEBOUNCE` 进行按钮去抖

`DEBOUNCE` 用于过滤机械按钮触点产生的短噪声脉冲。
仅当 `IN` 在完整的 `T_Debounce` 持续时间内保持稳定时，`Q` 才会
切换 —— 适用于上升沿和下降沿。

### 引脚布局

| 引脚 | 方向 | 类型 | 含义 |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | 原始输入（通常是 `%IX`，存在机械抖动） |
| `tDebounce`  | INPUT  | `TIME` | 最小稳定时间（通常 `T#10ms`...`T#50ms`） |
| `Q`          | OUTPUT | `BOOL` | 去抖后的输出 |

### 代码示例

PROGRAM 主体对 `%IX0.0` 上的按钮去抖，并将去抖后的信号
作为单脉冲边沿转发给一个自保持接触器：

```text
PROGRAM PLC_PRG
VAR
    button_raw      AT %IX0.0 : BOOL;       (* bouncing contact *)
    button_clean    : BOOL;                  (* after DEBOUNCE *)
    button_pressed  : BOOL;                  (* single-shot per press *)
    relay_lamp      AT %QX0.0 : BOOL;        (* lamp as self-hold *)
    fbDeb           : DEBOUNCE;              (* instance *)
    fbTrig          : R_TRIG;                (* edge detector *)
END_VAR

fbDeb(IN := button_raw, tDebounce := T#20ms);
button_clean := fbDeb.Q;

fbTrig(CLK := button_clean);
button_pressed := fbTrig.Q;

(* Self-hold: toggle on every rising edge *)
IF button_pressed THEN
    relay_lamp := NOT relay_lamp;
END_IF;
END_PROGRAM
```

`DEBOUNCE` 内部由两个 `TON` 块构成（高、低两个方向）—— 一个仅在
`IN` 持续保持有效达到 `T_Debounce` 后才把 `Q` 置 TRUE，另一个仅在
`IN` 持续无效达到 `T_Debounce` 后才把 `Q` 置 FALSE。这使得过滤器
对称：无论是按下还是释放时的触点抖动都不会产生毛刺。

> **典型用途：** 机械按钮、限位开关、基于触点的传感器。
> 若需要"每次按下输出一个脉冲"——如上例所示——
> 在 `Q` 之后串接一个 `R_TRIG`。

## 示例 2 —— 带模式覆盖的自保持（`JK_FF`）

`JK_FF` 是一个带内置按钮去抖的翻转触发器。每当 `xButton`
出现稳定的上升沿时，它就在 TRUE 与 FALSE 之间翻转 `Q` ——
这样普通按钮就成为一个"开/关"开关，**无需**应用程序手动
将 DEBOUNCE + R_TRIG + 切换逻辑串联起来。

### 引脚布局

| 引脚 | 方向 | 类型 | 含义 |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | 原始按钮触点（带抖动） |
| `tDebounce`  | INPUT  | `TIME` | 去抖时间（通常 `T#20ms`） |
| `J`          | INPUT  | `BOOL` | "Set"（激活时强制 `Q` 为 TRUE） |
| `K`          | INPUT  | `BOOL` | "Reset"（激活时强制 `Q` 为 FALSE） |
| `Q`          | OUTPUT | `BOOL` | 当前状态 |
| `Q_N`        | OUTPUT | `BOOL` | 取反状态（`NOT Q`） |
| `xStable`    | OUTPUT | `BOOL` | 当 `xButton` 已稳定 `tDebounce` 时为 TRUE |

### 代码示例

带三个按钮的灯具控制：`T1` 切换灯具，`T_Mains` 强制开灯
（例如"全部主灯打开"），`T_Off` 强制全部关闭：

```text
PROGRAM PLC_PRG
VAR
    bButtons     AT %IX0.0 : ARRAY [0..3] OF BOOL;
    relay_lamp   AT %QX0.0 : BOOL;
    fbToggle     : JK_FF;
END_VAR

fbToggle(
    xButton    := bButtons[0],   (* toggle button T1 *)
    tDebounce  := T#20ms,
    J          := bButtons[1],   (* main light ON while held *)
    K          := bButtons[2]    (* main light OFF while held *)
);

relay_lamp := fbToggle.Q;
END_PROGRAM
```

`J`/`K` 输入的真值表：

| `J` | `K` | 行为 |
|---|---|---|
| FALSE | FALSE | 每次去抖按下时切换 |
| TRUE  | FALSE | Q := TRUE（置位，覆盖切换） |
| FALSE | TRUE  | Q := FALSE（复位，覆盖切换） |
| TRUE  | TRUE  | 未定义 —— 应避免 |

`xStable` 可用于实现"按钮当前正被按住"逻辑（例如可视化按下状态的
LED，无需等待切换效果生效）。

## 编辑器与 PLC 之间的库同步

标准库存在于两处：

  - **编辑器侧：** `editor/resources/library/standard_library.json`
    （通过 Qt 资源系统编译进 `.exe`）。
  - **PLC 侧：** anvild 子模块，相同的 JSON 文件，由 `make` 步骤
    在已上传的 C 源代码中包含。

**库同步**在连接时比较两个版本的 SHA-256。当出现不一致时，
Output 面板会显示提示；响应方式可配置：

  - `Preferences > Library > Auto-Push` 关闭（默认）：通过
    `Tools > Sync Library` 手动推送。可保护生产运行时免受
    较旧编辑器的意外覆盖。
  - `Preferences > Library > Auto-Push` 开启：检测到不一致时
    自动推送。适用于单一程序员的开发环境。

## ForgeIEC 扩展

下列块在 IEC 61131-3 中并未标准化，但作为标准库的一部分
随产品提供，因为它们在实践中被证明普遍有用：

| 块 | 用途 |
|---|---|
| `JK_FF` | 带内置按钮去抖的翻转触发器（参见示例 2）。 |
| `DEBOUNCE` | 对称式按钮去抖（参见示例 1）。 |

这些块位于 *Standard Function Blocks / Application* 下，在 JSON
源中标记为 `isStandard: true`，被视为"不可删除"
（即不能通过库面板意外移除）。

## 将自定义块添加到用户库

当前项目中每个 `FUNCTION_BLOCK` 和 `FUNCTION` 声明都会自动出现在
**用户库**下。可见时机：

  1. **库面板中：** 声明并保存 POU 后立即可见。
  2. **代码补全器（Ctrl-Space）：** 立即可用。
  3. **FBD/LD 编辑器中作为块：** 立即可用。
  4. **PLC 上：** 在 `Compile + Upload` 之后可用。

要跨项目重用某个块，可通过 `File > Export POU...` 将该 POU
导出为 `.forge-pou` 文件，并在目标项目中导入 ——
跨项目的"工作区库"已列入待办。

## 相关主题

- [Structured Text 语法](../st/) —— ST 中块调用的写法。
- [Function Block Diagram 编辑器](../fbd/) —— 块的图形化连线方式。
- [变量面板](../variables/) —— 地址池如何看待实例。
