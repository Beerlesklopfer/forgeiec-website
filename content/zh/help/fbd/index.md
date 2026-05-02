---
title: "Function Block Diagram 编辑器（FBD）"
summary: "函数、功能块和变量的图形化连线"
---

## 概述

Function Block Diagram (FBD) 是 ForgeIEC Studio 支持的三种图形化
IEC 61131-3 语言之一。一个 FBD 程序由**函数与功能块调用**通过
**显式连线**互连而成 —— 同时也连接到输入和输出变量。
与 Ladder Diagram 不同，FBD **没有电源母线**：每条连线都是单根
导线，将一个输出引脚送到一个或多个输入引脚。

## 编辑器布局

FBD 编辑器是三部分组合的控件：

```
+---------------------------------------------+
| Toolbar (Select | Wire | Block | Var | ...) |
+--------------------------------+------------+
|                                |            |
|       QGraphicsView            |  Variable  |
|       Grid + Zoom + Pan        |  table     |
|                                |  (right)   |
|                                |            |
+--------------------------------+------------+
```

* **顶部工具栏：** 工具切换（Select、Wire、Place Block、
  Place In-/Out-Variable、Comment、Zoom）。
* **QGraphicsView：** 绘图区，带背景网格
  （次网格 10 px，主网格 50 px）和中键平移。鼠标滚轮以光标
  为中心缩放。
* **右侧变量表：** 可停靠，显示 POU 的局部变量。从该表的
  拖放操作会在编辑器中创建一个输入/输出变量项。

## 工具

| 工具 | 效果 |
|---|---|
| **Select** | 选取、移动、删除项。 |
| **Wire** | 单击一个输出端口，再单击一个输入端口 —— 连接被建立。 |
| **Place Block** | 从库中放下一个函数或功能块。引脚列表（输入在左，输出在右）取自库定义。 |
| **InVar / OutVar** | 放置一个输入或输出变量项。名称通过对话框输入，可以是 GVL、Anvil 或 Bellows 限定的变量。 |
| **Comment** | 自由文本注释，无语义影响。 |

## 块和引脚

**块项**代表对函数（`ADD`、`SEL`、…）或功能块
（`TON`、`CTU`、…）的调用。该项在头部显示类型名，
下方是实例名（仅 FB），两侧是端口：

```
        +---- TON -----+
        | tonA         |
   IN --| IN          Q|-- timeUp
   PT --| PT         ET|-- elapsed
        +--------------+
```

输入**始终在左**，输出**始终在右**。
取反引脚在端口处用一个小圆圈标识。

## 库拖放

在库面板中，任何标准块或用户块都可**直接拖放至编辑器**。
释放时引脚列表取自库定义；对于功能块，编辑器会
自动在局部变量段中创建一个 `VAR` 实例条目。

## 与 ST 之间的往返转换

在编译时 ForgeIEC 编译器会把 FBD 主体翻译为
Structured Text。块按数据流进行拓扑排序以确定执行顺序。
因此：**任何 FBD 主体在语义上等价于一个 ST 主体**，
语言的选择纯粹是可读性问题。

## 示例 —— 使用 `TON` 的接通延时定时器

`TON`（接通延时定时器）按可配置的时间延迟输入信号。
在 FBD 中您将：

  * 把**输入变量** `start` 连到 `TON` 实例的 `IN` 引脚，
  * 把值为 `T#5s` 的**输入变量**连到 `PT` 引脚，
  * 把 `Q` 输出连到**输出变量** `lampe`。

在 ST 中如下：

```text
PROGRAM PLC_PRG
VAR
    start  AT %IX0.0 : BOOL;
    lampe  AT %QX0.0 : BOOL;
    tmr    : TON;
END_VAR

tmr(IN := start, PT := T#5s);
lampe := tmr.Q;
END_PROGRAM
```

这正是编译器从 FBD 图生成的形式 ——
变量实例 `tmr` 即 `Block` 框，两条线即两个 `:=` 赋值。

## 相关主题

* [库](../library/) —— 块选择器提供的块。
* [变量面板](../variables/) —— 变量声明与地址池。
* [Ladder Diagram](../ld/) —— 面向电流路径的姊妹语言。
