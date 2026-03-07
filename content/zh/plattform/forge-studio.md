---
title: "Forge Studio"
description: "IEC 61131-3 开发环境 -- 专业的 PLC 编程 IDE"
weight: 1
---

## Forge Studio -- 工业自动化 IDE

Forge Studio 是 ForgeIEC 的集成开发环境，用于按照 IEC 61131-3 标准进行 PLC
编程。基于 C++17 和 Qt6 开发，为所有 PLC 编程任务提供工业级工具。

---

## 五种 IEC 61131-3 语言

一个编辑器支持所有语言 -- 无缝切换，共享变量，统一的项目结构。

- **结构化文本 (ST)** -- 语法高亮、自动补全、查找和替换
- **指令表 (IL)** -- 完整的语言支持和智能编辑
- **功能块图 (FBD)** -- 带有功能块库的图形编辑器
- **梯形图 (LD)** -- 熟悉的开关逻辑表示方法
- **顺序功能图 (SFC)** -- 用于过程控制的步序图

---

## 编译与部署

Forge Studio 在工作站上本地编译 IEC 程序。生成的 C 文件通过加密的 gRPC 传输到
目标 PLC。PLC 只需要 C 编译器 -- 目标系统上不需要 IEC 编译器。

- 使用 `iec2c` 本地编译（IEC 61131-3 到 C）
- 加密传输到目标系统
- 自动生成适配平台的 Makefile
- 支持 x86_64、ARM64 和 ARMv7 架构

---

## 工业总线系统

CoDeSys 风格的现场总线配置，具有段层次结构和自动设备发现。

- **Modbus TCP** -- 以太网通信
- **Modbus RTU** -- RS-485 串行连接
- **EtherCAT** -- 实时以太网现场总线
- **Profibus DP** -- 成熟的工业标准
- 自动 IEC 地址分配，无冲突
- 网络扫描器用于设备发现

---

## 实时调试

- PLC 运行时实时观察变量
- 无需停产即可强制变量值
- 带过滤功能的监控面板

---

## 标准库

完整的 IEC 标准库：计数器、定时器、边沿检测、类型转换和数学函数。可通过
用户自定义功能块进行扩展。存储在 SQLite 数据库中，提供快速访问和高效搜索。

---

## 用户管理

- 使用 bcrypt 加密的密码认证
- 用于会话的 JWT 令牌
- CoDeSys 风格的首次登录
- 基于角色的访问控制

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio -- 为工业编程。开源。**

blacksmith@forgeiec.io

</div>
