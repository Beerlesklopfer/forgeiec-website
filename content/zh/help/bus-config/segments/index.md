---
title: "总线段"
summary: "现场总线段的配置（PLC 一个接口上的一个物理网络）"
---

## 概述

**总线段**描述的是 **PLC 目标的一个接口上的一个物理网络** ——
通常是用于 Modbus TCP / EtherCAT / EtherNet-IP 的以太网端口
（`eth0`、`enp3s0`），或用于 Modbus RTU / Profibus DP 的串口
（`/dev/ttyUSB0`）。对于每个段，`anvild` 守护进程会启动**恰好一个
桥接进程**（`tongs-modbustcp`、`tongs-ethercat`、…），负责处理
该段中所有设备的通信。

一个项目可包含任意数量的段 —— 每个段都有自己的协议、
自己的接口和自己的轮询节奏。例如，一个快速 EtherCAT
轴控制器（`eth1`，1 ms）和一个慢速 Modbus TCP 传感器轮询器
（`eth0`，100 ms）可以在同一个项目中并行运行。

## 段的字段

结构定义位于 `editor/include/model/FBusSegmentConfig.h`。
段在 `.forge` 项目中以 `<fi:segment>` 形式持久化于
`<fi:busConfig>` 内（参见[总线配置](../)）。

### 标识 + 协议

| 字段 | 类型 | 含义 |
|---|---|---|
| `segmentId` | UUID | 稳定的主键 —— 创建时自动生成，不可编辑。重命名、协议变更和 IP 变更后都保持不变。 |
| `protocol` | enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`。决定启动哪个桥接守护进程。 |
| `name` | string | 用户标签（例如 `"Fieldbus Hall 1"`）。自由格式，显示在树和日志中。 |
| `enabled` | bool | 开关。`false` = 桥接不启动，设备保持离线。默认值：`true`。 |

### 接口 + 路由

| 字段 | 类型 | 含义 |
|---|---|---|
| `interface` | string | 网络接口（`eth0`、`enp3s0`、`/dev/ttyUSB0`）。由桥接传递给 socket / 串口 API。 |
| `bindAddress` | string (IP/CIDR) | 出向 TCP 连接的源 IP，例如 `192.168.24.100/24`。为空 = 操作系统选择该接口的第一个 IP。 |
| `gateway` | string (IP) | 离开本地子网时数据包的默认网关。为空 = 无网关。 |
| `pollIntervalMs` | int (ms) | 桥接轮询间隔。`0` = 尽可能快（忙循环 / 实时）。典型值：Modbus TCP 为 `100`，EtherCAT 为 `0`。 |

### 网络设置（高级）

这些字段是在网络设置开发周期中加入的，用于覆盖操作系统默认值
不够用的场景 —— 通常是：每个从站需要大量并行 TCP 连接、
NAT 后的长寿命 TCP 会话，或单张网卡上承载多个子网。

| 字段 | 类型 | 含义 |
|---|---|---|
| `subnetCidr` | string (CIDR) | 段的本地子网，例如 `192.168.24.0/24`。当绑定网卡承载多个网络时，可让桥接正确路由每设备网关覆盖。 |
| `sourcePortRange` | string `"min-max"` | 出向连接的 TCP 源端口池，例如 `30000-39999`。为空 = 操作系统从临时端口范围选择。当需要对同一从站建立大量并行连接时（每个连接对应一个源端口）非常重要。 |
| `keepAliveIdleSec` | int (s) | 发送第一次 TCP keep-alive 探测前的空闲秒数。`0` = 操作系统默认值。 |
| `keepAliveIntervalSec` | int (s) | keep-alive 探测之间的间隔。`0` = 操作系统默认值。 |
| `keepAliveCount` | int | 在连接被判定为已断开之前允许的失败探测次数。`0` = 操作系统默认值。 |
| `maxConnections` | int | 连接池上限。`0` = 不限。对于具有硬性连接数上限的从站非常有用。 |
| `vlanId` | int (1..4094) | 出向帧的 802.1Q VLAN 标签。`0` = 不打标签。 |

### 协议特定设置

`settings` 映射（键/值）保存仅对某一特定协议有意义的值 ——
例如 Modbus TCP 的 `port`、`timeout_ms`；Modbus RTU 的
`serial_port`、`baud_rate`、`parity`、`stop_bits`；Profibus 的
`master_address`。`log_level` 和 `log_file` 也以协议无关的方式
保存在同一映射中。

## 编辑流程

在总线树面板中两条路径等价 —— 它们操作同一字段集，
具有相同的语义效果：

| 操作 | 效果 |
|---|---|
| **单击**段节点 | `FPropertiesPanel`（默认停靠：右侧）将所有字段显示为内联编辑器 —— 在 `editingFinished` 时变更被写入项目并将项目标记为脏。 |
| **双击**段节点 | 打开模态 `FSegmentDialog`，包含相同的字段集，分组为 *General* / *Modbus TCP* / *Advanced Network* / *Logging*。OK 提交，Cancel 丢弃。 |

## 示例：Modbus TCP 段

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

此段在 `eth0` 上以源 IP `192.168.24.100` 启动 `tongs-modbustcp`，
每 100 ms 轮询所有设备，并对每个请求接受最多 2000 ms 的
响应时间，超过则在状态流上发出超时错误。

## 相关主题

* [总线配置 —— 模式概览](../) —— XML 持久化和
  PLCopen `<addData>` 机制。
* [总线设备](../devices/) —— 段内的设备。
* [项目文件格式](../../file-format/) —— `.forge` XML 根。
