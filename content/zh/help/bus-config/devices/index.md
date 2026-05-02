---
title: "总线设备"
summary: "总线段内设备的配置（Modbus 从站、EtherCAT 从站、…）"
---

## 概述

**总线设备**是**段内的单个设备** —— 通常是 Modbus TCP 从站
（I/O 模块、驱动器）、EtherCAT 从站（伺服轴、I/O 耦合器）、
Profibus DP 从站或 EtherNet-IP 适配器。对于每个设备，
负责的桥接维护一条逻辑连接，按配置轮询寄存器，
并通过 Anvil IPC 组将数据发布给 PLC 运行时。

一个设备可以是**模块化的**：总线耦合器（slot 0）携带 1..N 个
位于 slot 1..N 的 I/O 模块。没有扩展槽的紧凑设备拥有空的
`modules` 列表 —— 此时变量直接位于 slot 0 上。

## 设备的字段

结构定义位于 `editor/include/model/FBusSegmentConfig.h`
（紧邻段定义）。设备在 `.forge` 项目中以 `<fi:device>` 形式
持久化于 `<fi:segment>` 内（参见[总线配置](../)）。

### 标识 + 寻址

| 字段 | 类型 | 含义 |
|---|---|---|
| `deviceId` | UUID | 稳定的主键 —— 创建时自动生成。在主机名重命名和 IP 变更时保持不变，从而保持所有变量绑定稳定。 |
| `hostname` | string | 用户可见标签（`"Maibeere"`、`"Stachelbeere"`）。DHCP 安全，但显式地**不是**主键。 |
| `ipAddress` | string (IP) | IP 地址（Modbus TCP / EtherNet-IP）。无 IP 的设备为空（EtherCAT 从站通过总线位置标识自身）。 |
| `port` | int | TCP 端口。默认 `502`（Modbus TCP）。 |
| `slaveId` | int | Modbus 从站 ID（1..247）。在 TCP 上通常为 `1`。 |
| `anvilGroup` | string | 用于桥接和 PLC 运行时之间零拷贝传输的 Anvil IPC 组。约定：与 `hostname` 同名。 |
| `catalogRef` | string | 描述设备的可选 FDD 目录条目引用（`"WAGO-750-352"`）。 |
| `description` | string | 自由文本描述（`"Bewaesserungsventil Sued"`）。 |

### 模块（槽）

| 字段 | 类型 | 含义 |
|---|---|---|
| `modules` | `FBusModuleConfig` 列表 | 设备的 I/O 模块。Slot 0 = 耦合器 / 紧凑设备，Slot 1..N = 扩展模块。每个模块包含：`slotIndex`、`catalogRef`、`name`、`baseAddress`、`settings`。 |

### 每设备覆盖

这些字段仅针对**该**设备覆盖段的对应值。`0` 或空字符串表示
*从段继承*。在属性面板中它们位于 *Advanced Overrides* 块下，
通常处于折叠状态。

| 字段 | 类型 | 含义 |
|---|---|---|
| `mac` | string `AA:BB:CC:DD:EE:FF` | 用于静态 ARP / 身份校验的 MAC 地址。可防止 DHCP 设备上的 IP 盗用。 |
| `endianness` | enum | 多寄存器值的字/字节序：`"ABCD"`（大端，IEC 默认值）、`"DCBA"`（字交换）、`"BADC"`（字节交换）、`"CDAB"`（字节 + 字交换）。为空 = 从段继承。 |
| `timeoutOverrideMs` | int (ms) | 每设备超时。`0` = 使用段超时。 |
| `retryCount` | int | 每个请求的重试次数。`0` = 段默认值。 |
| `connectionMode` | enum | `"always"`（在周期之间保持 TCP 打开）或 `"on_demand"`（每次事务重新连接）。为空 = 段 / 桥接默认值。 |
| `gatewayOverride` | string (IP) | 当设备所在子网与绑定网卡不同时，为该设备使用的网关。 |

### 设备特定设置

`settings` 映射（键/值）保存仅对此设备或其设备类型有意义的值 ——
例如驱动器的某个阈值或首选的功能码。

## 编辑流程

| 操作 | 效果 |
|---|---|
| **单击**设备节点 | `FPropertiesPanel` 将所有字段显示为内联编辑器 —— General 块（hostname、IP、port、slave ID、Anvil 组）、Override 块（MAC、超时、重试、字节序、连接模式、网关覆盖、描述）以及状态表。 |
| **双击**设备节点 | 打开模态 `FBusDeviceDialog`，包含相同的字段集。在编辑模式下"Import from catalog"按钮被锁定，以避免后续 FDD 导入悄无声息地覆盖现有 I/O 变量绑定。 |

## 状态变量（只读）

运行时每个设备都会发布一个状态结构，由守护进程通过 gRPC
状态流发送。这些值在属性面板中显示为**只读表**，**不可**从 UI
编辑 —— 由桥接写入。在 ST 代码中它们仍可作为
`anvil.<seg>.<dev>.Status.*` 下的限定路径访问：

| 状态变量 | 类型 | 含义 |
|---|---|---|
| `xOnline` | `BOOL` | 设备当前可达（最近一次请求得到响应）。 |
| `eState` | `INT` | 状态枚举：0=offline，1=connecting，2=online，3=error。 |
| `wErrorCount` | `WORD` | 自桥接启动以来失败请求的计数。 |
| `sLastErrorMsg` | `STRING` | 最近的错误消息（超时、Modbus 异常、…）。 |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## 示例：带两个槽的 WAGO 750 总线耦合器

一个 Modbus TCP 总线耦合器 750-352，slot 1 上一个 8-DI 模块（750-430），
slot 2 上一个 8-DO 模块（750-530）：

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

8 个输入在地址池中以 `%IX0.0..%IX0.7` 出现，
`deviceId="0e5d5537-..."`、`moduleSlot=1` 和 `modbusAddress=0..7`。
8 个输出同理，`moduleSlot=2`。

## 相关主题

* [总线段](../segments/) —— 设备所在的网络。
* [总线配置 —— 模式概览](../) —— XML 持久化。
* [项目文件格式](../../file-format/) —— 地址池和
  变量到设备的绑定。
