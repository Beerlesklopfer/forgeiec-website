---
title: "Bellows"
description: "OPC UA 网关，用于机器对机器通信"
weight: 3
---

## Bellows -- OPC UA 网关

**开发中**

Bellows 是 ForgeIEC 平台的 OPC UA 网关。铁匠铺的风箱为火焰提供动力 -- Bellows
为自动化系统与 IT 基础设施之间的通信提供动力。

---

## 机器对机器通信

OPC UA（开放平台通信统一架构）是工业 4.0 的通信标准。Bellows 将提供一个完整的
OPC UA 服务器，将 PLC 变量暴露给上层系统。

### 预计应用场景

- **SCADA 集成** -- 将 PLC 连接到现有的监控系统
- **M2M 数据交换** -- PLC 与第三方系统之间的直接通信
- **IT/OT 网关** -- 自动化网络与 IT 基础设施之间的桥梁
- **数据归档** -- 为存档提供过程数据

---

## 计划架构

Bellows 将作为独立进程运行，由 `anvild` 守护进程管理。过程数据通过 Anvil
（零拷贝 IPC）接收，并通过 OPC UA 协议暴露。

```
PLC  --->  anvild  --->  Bellows (OPC UA 服务器)  --->  OPC UA 客户端
            Anvil IPC                                    SCADA, MES, 云
```

### 计划功能

- 符合规范的 OPC UA 服务器
- IEC 变量自动暴露
- 可配置的信息模型
- 加密和认证
- 自动服务发现
- 内置数据历史记录

---

## 安全性

- 所有连接的 TLS 加密
- 证书或密码认证
- 按变量的细粒度访问控制
- 符合 OPC UA 安全配置文件

---

<div style="text-align:center; padding: 2rem;">

**Bellows 正在开发中。信息将随着项目进展而更新。**

blacksmith@forgeiec.io

</div>
