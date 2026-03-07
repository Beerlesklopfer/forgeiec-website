---
title: "Anvil"
description: "实时 PLC 运行时，具有零拷贝 IPC"
weight: 2
---

## Anvil -- 锻造的核心

在每一个铁匠铺中，铁砧都是核心工具 -- 在这里金属被塑形、淬火和精炼。**Anvil**
是 PLC 运行时和协议桥接器之间的中间层。您的过程数据在这里被锻造：接收、转换
并分配到正确的接收者。

Anvil 使用专有的零拷贝共享内存传输层进行进程间通信。无序列化，无拷贝，
无妥协。

---

## 架构

```
+--------------+         +------------+         +------------------+
|              |         |            |         |                  |
| PLC 程序     |<------->|  anvild    |<------->|  Modbus 桥接器   |---> 现场设备
| (IEC 代码)   |  gRPC   |  (守护进程) |  Anvil  |  EtherCAT 桥接器 |---> 驱动器
|              |         |            |         |  Profibus 桥接器  |---> 传感器
+--------------+         +------------+         |  OPC-UA 桥接器   |---> SCADA
                                                +------------------+

                         <--- Anvil --->
                          零拷贝 IPC
                           共享内存
```

`anvild` 与协议桥接器之间的数据交换通过 **Anvil** 进行 -- 这是一个基于零拷贝
共享内存的高性能 IPC 通道。每个段获得自己的通信通道。

---

## 为什么选择 Anvil？

### 微秒级延迟

传统 IPC 机制（管道、套接字、消息队列）在进程间复制数据。Anvil 消除了每一次
拷贝。数据驻留在共享内存中 -- 接收者直接读取。

| 方法 | 典型延迟 | 拷贝次数 |
|------|---------|---------|
| TCP 套接字 | 50-200 微秒 | 2-4 |
| Unix 套接字 | 10-50 微秒 | 2 |
| **Anvil** | **< 1 微秒** | **0** |

### 工业级质量

- 确定性行为 -- 热路径中无动态内存分配
- 无锁算法 -- 无阻塞，无死锁
- 发布/订阅模型 -- 生产者和消费者之间松耦合
- 自动生命周期管理 -- 桥接器被监控并在崩溃时自动重启

### IEC 程序中的 PUBLISH/SUBSCRIBE

Anvil 无缝集成到 IEC 61131-3 编程中：

```iec
VAR_GLOBAL PUBLISH 'Motors'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensors'
    Temperature AT %IW0   : INT;
    Pressure    AT %IW2   : INT;
END_VAR
```

PUBLISH/SUBSCRIBE 关键字是 ForgeIEC 对 IEC 61131-3 标准的扩展。编译器自动生成
Anvil 绑定。

---

## 支持的协议

| 协议 | 桥接器 | 状态 |
|------|-------|------|
| **Modbus TCP** | `tongs-modbustcp` | 可用 |
| **Modbus RTU** | `tongs-modbusrtu` | 可用 |
| **EtherCAT** | `tongs-ethercat` | 开发中 |
| **Profibus DP** | `tongs-profibus` | 开发中 |
| **OPC-UA** | `tongs-opcua` | 计划中 |

每个桥接器作为独立进程运行。`anvild` 自动启动、监控和重启桥接器。一个桥接器的
崩溃不会影响 PLC 或其他桥接器。

---

## 技术细节

- **IPC 框架**：Anvil（专有零拷贝共享内存）
- **架构**：每个总线段一个发布者/订阅者通道
- **数据格式**：原始 IEC 变量 -- 无序列化，无开销
- **平台**：x86_64、ARM64、ARMv7（Linux）
- **进程模型**：每个活动段一个桥接器进程

---

<div style="text-align:center; padding: 2rem;">

**Anvil -- 数据在这里被锻造成控制指令。**

blacksmith@forgeiec.io

</div>
