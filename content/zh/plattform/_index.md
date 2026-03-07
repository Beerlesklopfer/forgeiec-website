---
title: "平台"
description: "ForgeIEC 平台 -- 工业自动化的全部组件"
weight: 10
---

## ForgeIEC 平台

ForgeIEC 是一个完整的工业自动化平台 -- 从开发环境到监控系统。每个组件都以铁匠
工具命名，因为 ForgeIEC 为工业而锻造。

---

### Forge Studio

**IEC 61131-3 开发环境**

专业的 PLC 编程 IDE。支持全部五种 IEC 语言，图形化和文本编辑，本地编译，远程
部署。基于 C++17 和 Qt6 构建。

[了解更多](forge-studio/)

---

### Anvil

**实时 PLC 运行时**

在目标系统上执行 IEC 程序的运行时守护进程。通过 Anvil 共享内存技术实现运行时
与协议桥接器之间的零拷贝通信。

[了解更多](anvil/)

---

### Bellows

**OPC UA 网关** -- 开发中

符合 OPC UA 标准的机器对机器通信。将自动化系统无缝集成到现有 IT 基础设施中。

[了解更多](bellows/)

---

### Hearth

**SCADA/HMI** -- 开发中

工业监控的过程可视化和人机界面。实时仪表盘、数据历史记录、报警管理。

[了解更多](hearth/)

---

### Spark

**Zenoh 隧道**

基于 Zenoh 协议的边缘到云端网络桥接。在现场 PLC 和云服务之间建立安全连接，
无需 VPN，无需复杂配置。

[了解更多](spark/)

---

### Tongs

**现场总线桥接器**

Modbus TCP/RTU、EtherCAT 和 Profibus DP 的协议桥接器。每个桥接器作为独立进程
运行，由运行时自动监控和重启。

[了解更多](tongs/)

---

### Ledger

**生产订单管理** -- 开发中

MES 集成，用于生产订单管理、生产跟踪和可追溯性。连接自动化与生产计划的桥梁。

[了解更多](ledger/)

---

<div style="text-align:center; padding: 2rem;">

**基于 OpenPLC** -- ForgeIEC 基于 [OpenPLC](https://autonomylogic.com/) 项目，完全兼容其文件架构。现有的 OpenPLC 项目可以直接打开和开发。

**所有组件均为开源。无许可费用。无供应商锁定。**

blacksmith@forgeiec.io

</div>
