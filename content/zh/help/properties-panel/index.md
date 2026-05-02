---
title: "属性面板"
summary: "针对项目树中所选总线元素的内联编辑器"
---

## 概述

**属性面板**是编辑器主窗口右侧的详情视图。
它显示**当前在项目树中所选元素的每个字段**，
并允许内联编辑这些字段 —— 无需为每次编辑打开
模态对话框。

```
Project tree                          Properties panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- click   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

**单击**树节点会立即渲染对应的字段列表 ——
**双击**会另外打开模态配置对话框
（[总线配置](../bus-config/)），字段集完全相同。

面板被包装在 `QScrollArea` 中并可垂直滚动：带 FDD
扩展和状态表的设备很容易达到 40+ 字段，所有这些字段
即使在停靠区较窄时也必须保持可达。

## 总线段

选择总线段时面板显示：

| 字段 | 含义 |
|---|---|
| **Name** | 项目树中的显示名称。 |
| **Protocol** | `modbustcp`、`modbusrtu`、`ethercat`、`profibus`、`ethernetip`。 |
| **Interface** | 桥接绑定的网络接口（`eth0`、`eth1`、…）。 |
| **Bind Address** | CIDR 表示法，例如 `192.168.1.10/24`。已校验。 |
| **Gateway** | 桥接进程的默认网关。 |
| **Poll Interval** | 桥接轮询其设备的周期，单位 `ms`。 |
| **Enabled** | 桥接子进程是否激活。 |

### 高级网络（全部可选）

镜像 `FSegmentDialog` 中相同的分组，并覆盖操作系统 / 桥接
默认值：

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count**（TCP 心跳）
  - **Max Connections** (`0` = 不限)
  - **VLAN ID** (`0` = 不打标签)

### 协议特定

| 协议 | 字段 |
|---|---|
| `modbustcp`  | `Port`（默认 `502`）、`Timeout`（`ms`，默认 `2000`）。 |
| `modbusrtu`  | `Serial Port`（例如 `/dev/ttyUSB0`）、`Baud Rate`、`Parity`（`none`/`even`/`odd`）。 |
| `profibus`   | `Serial Port`、`Baud Rate`（最高 12 Mbit/s）、`Master Address`（0..126）。 |

### 日志

  - **Log Level** —— `off` / `error` / `warn` / `info` / `debug`。
  - **Log File** —— 例如 `/var/log/forgeiec/segment.log`。为空 = stdout。

## 总线设备

| 字段 | 含义 |
|---|---|
| **Hostname** | DNS 或显示名称。 |
| **IP Address** | 设备的 IPv4 地址。 |
| **Port** | 从站上的 Modbus 端口（默认 `502`）。 |
| **Slave ID** | Modbus 单元 ID（0..247）。 |
| **Anvil Group** | Anvil IPC 组名 —— 同时也是自动生成的 `AnvilVarList` 的名称。重命名将同步重命名 GVL 标签、AnvilVarList 以及所有 `anvilGroup = oldGroup` 的池变量。 |

### 高级覆盖（全部可选，为空 = 从段继承）

  - **MAC Address** —— `AA:BB:CC:DD:EE:FF`。已校验。
  - **Endianness** —— `ABCD` / `DCBA` / `BADC` / `CDAB`。
  - **Timeout**（`ms`）。`0` = 从段继承。
  - **Retry Count**。`0` = 从段继承。
  - **Connection Mode** —— `always connected` 或 `on demand`。
  - **Gateway (override)** —— 仅当设备位于不同子网时使用。
  - **Description** —— 自由文本（例如 `South irrigation valve`）。

### 状态变量（只读）

每个设备都会自动公开通用故障模型 —— 通过 Anvil 以
只读状态主题发布的七个隐式字段：

| 名称 | IEC 类型 | 含义 |
|---|---|---|
| `xOnline`              | `BOOL`         | 当 `eState = Online` 或 `Degraded` 时为 TRUE。 |
| `eState`               | `eDeviceState` | 当前故障状态。 |
| `wErrorCount`          | `UDINT`        | 自桥接启动以来的错误总数。 |
| `wConsecutiveFailures` | `UDINT`        | 自最近一次 `Online` 起的失败次数（在 `Online` 时复位）。 |
| `wLastErrorCode`       | `UINT`         | `0` = 无；`1..99` 通用；`100+` 协议特定。 |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8，零填充。 |
| `tLastTransition`      | `ULINT`        | 最近一次状态转换的 Unix 时间（毫秒）。 |

当设备通过 `catalogRef` 绑定到 **FDD**（现场设备描述）时，
状态表会另外列出 FDD 定义的扩展，在 `Source` 列中标记为
`FDD +<offset>`。

在 ST 代码中每个状态变量都可作为
`anvil.<seg>.<dev>.Status.*` 访问：

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## 总线模块

总线模块是设备内部的 I/O 切片。面板显示：

### 元数据

  - **Module**（显示名称或 `catalogRef`）
  - **Slot**（设备内的插槽索引）
  - **Catalog**（FDD 引用，例如 `Beckhoff.EL2008`）
  - **Base Addr**（IEC 基地址偏移）

### IO 变量表

列出每个 `busBinding.deviceId` 与 `busBinding.moduleSlot`
匹配此模块的池变量。列：

| 列 | 内容 |
|---|---|
| **Name** | 池名称（可编辑，例如 `Motor_Run`）。 |
| **Type** | IEC 类型（可编辑，例如 `BOOL`、`INT`）。 |
| **Address** | IEC 地址（`%IX0.0`，只读）。 |
| **Bus Addr** | Modbus 寄存器偏移（只读）。 |
| **Dir** | `in` 或 `out`（只读）。 |

排序：先输入再输出，然后按总线地址升序。

## 编辑行为

面板中的每次编辑都直接作用于模型：

  1. 在控件上编辑（`editingFinished` / `valueChanged` / `toggled`）。
  2. 模型字段被更新（`seg->name = ...`）。
  3. `project->markDirty()` 抬起脏标志。
  4. 发出 `busConfigEdited` 信号。
  5. 主窗口在需要时刷新项目树标签。

**没有**显式的 `Apply`，**也没有** `Cancel` —— 编辑立即生效。
在项目树上 `Ctrl+Z`（撤销）会回退最近一次编辑。

## 相关主题

  - [总线配置](../bus-config/) —— 与之具有相同字段集的模态对话框，
    适合编辑量大的高级用户。
  - [变量面板](../variables/) —— 为 `IO 变量`表提供数据的池。
