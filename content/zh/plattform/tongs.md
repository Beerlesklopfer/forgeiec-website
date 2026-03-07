---
title: "Tongs"
description: "现场总线桥接器 -- Modbus、EtherCAT、Profibus"
weight: 6
---

## Tongs -- 现场总线桥接器

铁钳是铁匠夹持灼热金属的工具。**Tongs** 夹取现场设备的数据并将其传输到 PLC
运行时。每种现场总线协议都有自己的桥接器，作为独立进程运行。

---

## 支持的协议

### Modbus TCP

Modbus 设备的以太网通信。读写寄存器、线圈和离散输入。内置网络扫描器用于自动
设备发现。

| 属性 | 值 |
|------|-----|
| 传输 | TCP/IP（以太网） |
| 桥接器 | `tongs-modbustcp` |
| 功能码 | FC1、FC2、FC3、FC4、FC5、FC6、FC15、FC16 |
| 状态 | 可用 |

### Modbus RTU

RS-485 上 Modbus 设备的串行通信。与 Modbus TCP 相同的功能，适配串行传输。

| 属性 | 值 |
|------|-----|
| 传输 | 串行 RS-485 |
| 桥接器 | `tongs-modbusrtu` |
| 状态 | 可用 |

### EtherCAT

用于驱动器、伺服电机和高性能 I/O 模块的实时以太网现场总线。

| 属性 | 值 |
|------|-----|
| 传输 | 以太网（实时） |
| 桥接器 | `tongs-ethercat` |
| 状态 | 开发中 |

### Profibus DP

用于现有设施中现场设备通信的成熟工业标准。

| 属性 | 值 |
|------|-----|
| 传输 | RS-485 / 光纤 |
| 桥接器 | `tongs-profibus` |
| 状态 | 开发中 |

---

## 架构

每个桥接器作为独立进程运行，由 `anvild` 守护进程管理。与运行时的通信通过
Anvil（零拷贝 IPC）进行。一个桥接器的崩溃不会影响 PLC 或其他桥接器。

```
anvild
  |
  +-- tongs-modbustcp --segment mb1 --> Modbus TCP 设备
  |
  +-- tongs-modbusrtu --segment mb2 --> Modbus RTU 设备
  |
  +-- tongs-ethercat  --segment ec1 --> EtherCAT 设备
  |
  +-- tongs-profibus  --segment pb1 --> Profibus 设备
```

### 进程管理

- 运行时启动时自动启动桥接器
- 持续监控 -- 崩溃时自动重启
- 每个活动总线段一个进程
- 每个桥接器独立日志

---

## 配置

总线段在目标系统的 `config.toml` 中配置。每个段定义协议、网络接口和连接的设备。

### I/O 变量

每个设备暴露输入和输出变量：

- **方向 "in"** -- 从设备读取（Subscribe）
- **方向 "out"** -- 向设备写入（Publish）
- 自动 IEC 地址分配（%I、%Q），无冲突

---

<div style="text-align:center; padding: 2rem;">

**Tongs -- 夹取现场数据的铁钳。**

blacksmith@forgeiec.io

</div>
