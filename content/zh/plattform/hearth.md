---
title: "Hearth"
description: "工业过程可视化的 SCADA/HMI"
weight: 4
---

## Hearth -- SCADA/HMI

**开发中**

Hearth 是 ForgeIEC 平台的监控和人机界面系统。炉膛是铁匠铺的中心，火焰在这里
燃烧 -- Hearth 是监控的中心，过程在这里被可视化。

---

## 过程可视化

工业自动化系统需要监控界面来观察、控制和诊断生产过程。Hearth 将提供这一可视化
层。

### 计划功能

- **实时仪表盘** -- 过程变量可视化，实时更新
- **过程画面** -- 使用工业符号的设施图形化表示
- **数据历史记录** -- 长期趋势的记录和显示
- **报警管理** -- 报警检测、通知和确认
- **报表** -- 自动生成生产报表

---

## 计划架构

Hearth 将作为 Web 应用运行，可从网络中的任何浏览器访问。过程数据将通过
OPC UA（Bellows）接收，或通过 gRPC 直接从运行时接收。

### 计划组件

- 响应式 Web 界面（桌面和平板电脑）
- 内置过程画面编辑器
- 可配置的报警引擎
- 历史数据库
- 用户权限和配置文件系统

---

## 平台集成

Hearth 将与 ForgeIEC 平台的其他组件集成：

- **Anvil** -- 实时过程数据
- **Bellows** -- 标准 OPC UA 通信
- **Ledger** -- 生产数据和制造订单
- **Forge Studio** -- 从 IDE 进行配置

---

<div style="text-align:center; padding: 2rem;">

**Hearth 正在开发中。信息将随着项目进展而更新。**

blacksmith@forgeiec.io

</div>
