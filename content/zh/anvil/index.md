---
title: "Anvil"
summary: "您的数据在我们的铁砧上锻造"
---

## 铁砧：每座锻造炉的核心

在每座锻造炉中，铁砧是核心工件——在这里金属被塑造、淬火和精炼。
**Anvil** 是 PLC 运行时与现场总线桥接器之间的中间层。您的过程数据在这里
被锻造：接收、转换并分发给正确的接收者。

Anvil 内部基于 **IceOryx2** 构建——一个用于进程间通信的零拷贝共享内存框架。
无序列化，无拷贝，无妥协。

---

## 架构

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│  PLC 程序    │◄───────►│  forgeiecd  │◄───────►│  Modbus 桥接     │──► 现场设备
│  (IEC 代码)  │  gRPC   │  (守护进程) │  Anvil  │  EtherCAT 桥接   │──► 驱动器
│              │         │            │ IceOryx2│  Profibus 桥接    │──► 传感器
└──────────────┘         └────────────┘         │  OPC-UA 桥接     │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                          零拷贝 IPC
                          共享内存
```

`forgeiecd` 与协议桥接器之间的数据交换通过 **Anvil** 进行——
一个基于 IceOryx2 共享内存的高性能 IPC 通道。
每个段拥有独立的通信通道。

---

## 为什么选择 Anvil？

### 微秒级延迟

传统 IPC 机制（管道、套接字、消息队列）在进程间复制数据。
Anvil 消除了所有复制。数据驻留在共享内存中——接收方直接读取。

| 方法 | 典型延迟 | 拷贝次数 |
|------|---------|---------|
| TCP 套接字 | 50–200 微秒 | 2–4 |
| Unix 套接字 | 10–50 微秒 | 2 |
| **Anvil (IceOryx2)** | **< 1 微秒** | **0** |

### 工业级品质

- 确定性行为——热路径中无动态内存分配
- 无锁算法——无阻塞，无死锁
- 发布/订阅模型——生产者与消费者松耦合
- 自动生命周期管理——桥接器被监控并在崩溃时自动重启

### IEC 程序中的 PUBLISH/SUBSCRIBE

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

PUBLISH/SUBSCRIBE 关键字是 ForgeIEC 对 IEC 61131-3 标准的扩展。
编译器自动生成 IceOryx2 绑定。

---

## 支持的协议

| 协议 | 桥接器 | 状态 |
|------|--------|------|
| **Modbus TCP** | `forgeiec-modbustcp` | 可用 |
| **Modbus RTU** | `forgeiec-modbusrtu` | 可用 |
| **EtherCAT** | `forgeiec-ethercat` | 开发中 |
| **Profibus DP** | `forgeiec-profibus` | 开发中 |
| **OPC-UA** | `forgeiec-opcua` | 计划中 |

每个桥接器作为独立进程运行。`forgeiecd` 自动启动、监控和重启桥接器。

---

<div style="text-align:center; padding: 2rem;">

**Anvil——数据在此被锻造为控制命令。**

blacksmith@forgeiec.io

</div>
