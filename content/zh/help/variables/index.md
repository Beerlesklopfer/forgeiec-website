---
title: "变量管理"
summary: "作为 FAddressPool 中央视图的变量面板 —— 列、过滤器、批量操作、安全开关"
---

## 概述

**变量面板**是 **FAddressPool** 的中央视图 ——
ForgeIEC 项目中每个变量的唯一可信源。
每个变量在池中以其 IEC 地址（`%IX0.0`、`%QW3`、…）为键，
正好存在一次。诸如 GVL、AnvilVarList、HmiVarList
或 POU 接口等容器仅是池上的**视图** —— 没有变量
会同时存在于两个存储中。

```
FAddressPool  (single source of truth)
   |
   +-- FAddressPoolModel  (Qt table)
         |
         +-- FVariablesPanel  (filters + bulk ops + clipboard)
               |
               +-- Tree filter sets FilterMode + tag
```

面板停靠于主窗口底部，并立即把每次变更镜像到所有其他视图
（POU 编辑器、ST 编译器、PLCopen-XML 保存）。

## 列

表格有 **15 列**；每一列都可通过表头上下文菜单单独切换 ——
每个 POU 编辑器实例独立保存其列可见性。

| 列 | 内容 |
|---|---|
| **Name** | 程序员可见的名称。受限定的池条目以完整路径显示：`Anvil.Pfirsich.T_1`、`Bellows.Stachelbeere.T_Off`、`GVL.Motor.K1_Mains`。 |
| **Type** | IEC 基本类型或用户自定义类型。数组显示为 `ARRAY [0..7] OF BOOL`。 |
| **Direction** | IEC 变量类别：POU 局部变量为 `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP`；池全局变量为 `in`/`out`（由 `%I` 与 `%Q` 推导）。 |
| **Address** | IEC 地址 —— 主键。位输入为 `%IX0.0`，字输出为 `%QW1`，标记位为 `%MX10.3`。 |
| **Initial** | 初始值（`FALSE`、`0`、`T#100ms`、`'OFF'`）。在第一个周期加载到变量中。 |
| **Bus Device** | 该变量所绑定的总线设备（Modbus 从站等）的 UUID —— 可作为下拉框编辑。 |
| **Bus Addr** | 相对从站的 Modbus 寄存器偏移（`0`、`1`、…）。 |
| **R** (Retain) | 复选框 —— 值是否在掉电后保留？ |
| **C** (Constant) | 复选框 —— IEC 常量（`VAR CONSTANT`），运行时不可写入。 |
| **RO** (ReadOnly) | 复选框 —— 程序代码只读。 |
| **Sync** | 多任务同步类（`L`/`A`/`D`），由最近一次 ST 编译器运行生成。 |
| **Used by** | 哪些任务读/写该变量，例如 `PROG_Fast (R/W), PROG_Slow (R)`。 |
| **Monitor** / **HMI** / **Force** | 每变量安全开关。后台中的 **Cluster A** —— 显式选择启用，与 `hmiGroup` 标签不同。在 codegen 之前 ST 编译器会校验：Force/HMI 访问只能针对带标志的变量。 |
| **Live** | 在线模式下的运行时值（由 anvild 实时值存储提供；断开连接时隐藏）。 |
| **Scope** | 示波器可见性复选框 —— 将变量发送到示波器面板。 |
| **Documentation** | 自由文本注释。 |

## 过滤模式

面板不会一次显示整个池 —— **左侧的项目树**决定可见的切片。
单击树节点会让主窗口设置 `FilterMode` 加标签：

| FilterMode | 显示 |
|---|---|
| `FilterAll` | 整个池 —— 无标签限制。 |
| `FilterByGvl` | `gvlNamespace == tag` 的变量（例如仅 `GVL.Motor`）。 |
| `FilterByAnvil` | `anvilGroup == tag` 的变量（一个 Anvil IPC 组）。 |
| `FilterByHmi` | `hmiGroup == tag` 的变量（一个 Bellows HMI 组）。 |
| `FilterByBus` | `busBinding.deviceId == tag` 的变量（某个总线设备的全部变量）。 |
| `FilterByModule` | 类似 `FilterByBus`，外加 `moduleSlot` —— 标签格式 `hostname:slot`。 |
| `FilterByPou` | POU 局部变量 —— `pouInterface == tag` 的变量。 |
| `FilterCommentsOnly` | 仅注释分隔符，无变量。 |

## 过滤轴（可组合）

表格上方有四个进一步的轴，与树过滤器叠加并并行作用：

  - **自由文本搜索**：覆盖名称、地址和标签 —— `to` 可找到 `T_Off`。
  - **IEC 类型过滤器**作为下拉（`all` / `BOOL` / `INT` / `REAL` / …）。
  - **地址范围过滤器**：`all` / `%I`（输入）/ `%Q`（输出）/
    `%M`（标记位）；在 `%M` 中进一步按字大小（`%MX` / `%MW` /
    `%MD` / `%ML`）。
  - **TaggedOnly 切换** —— 隐藏没有任何容器标签的池条目
    （便于查找"孤立"的池）。

每个过滤器以 AND 组合：未匹配所有激活轴的内容都会被隐藏。

## 多选 + 批量操作

如同任何 Qt 表格：Shift-click 和 Ctrl-click 选择范围或
单独的行。选区上的上下文菜单提供：

  - **Set Anvil Group...** —— 在每个所选变量上设置 `anvilGroup`。
  - **Set HMI Group...** —— 同上，针对 `hmiGroup`。
  - **Set GVL Namespace...** —— 同上，针对 `gvlNamespace`。
  - **Clear Tag** —— 清除当前过滤模式对应的标签。
  - **Toggle Monitor / HMI / Force** —— 批量切换安全开关。

每次批量编辑都通过 `FAddressPoolModel::applyToRows`，会产生
一次 `dataChanged` 信号，并作为单步撤销可以撤销。

## 剪贴板（复制 / 剪切 / 粘贴）

可复制选中变量 —— **包含所有标签和标志** —— 并粘贴到另一个
视图。负载使用两种格式：

  - **自定义 MIME**（`application/x-forgeiec-vars+json`）作为携带完整
    池信息的往返载体。
  - **TSV 纯文本**作为 Excel / 文本编辑器的回退方案。

**粘贴**时面板会自动将容器标签重新指向**当前过滤模式**：
从 `FilterByAnvil`（组 `Pfirsich`）复制并粘贴到 `FilterByHmi`
（组 `Stachelbeere`），变量将丢弃 `anvilGroup` 并获得
`hmiGroup = Stachelbeere`。冲突的地址和名称会被去重
（`T_1` → `T_1_1`）。

## 拖放到 HmiVarList

变量可从主面板拖入 HmiVarList POU。
随后编辑器会自动设置变量的 **HMI 导出标志**
并把 HMI 组写为标签 —— Bellows 导出已就绪。

## 每变量安全开关

三个每变量开关，每个都需显式启用：

  - **HMI** —— 允许 Bellows 读/写该变量。
  - **Monitor** —— 允许在线模式下实时观察。
  - **Force** —— 允许强制运行时值。

这些标志**与 `hmiGroup` 标签是分开的**。标签描述
组成员关系；标志启用效果。每次 codegen 之前 ST 编译器
都会验证：每个 Bellows 或 Force 访问都针对其标志已设置的变量 ——
否则会抛出编译错误。

## 相关主题

  - [添加变量](add/) —— `FAddVariableDialog`，支持范围模式
    和数组包装器。
  - [项目文件格式](../file-format/) —— 池在 PLCopen XML 中
    如何作为 `<addData>` 块持久化。
  - [库](../library/) —— 功能块如何在池中看到其实例。
