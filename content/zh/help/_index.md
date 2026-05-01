---
title: "帮助"
summary: "ForgeIEC 文档和资源"
---

## 帮助和资源

欢迎来到 ForgeIEC 帮助中心。在这里您可以找到关于我们项目基础
和理念的信息。

---

## 主题

### [总线配置](/help/bus-config/)

用于 `.forge` 项目中工业现场总线配置的 PLCopen XML 架构。
段、设备、变量绑定和 IEC 地址分配。

### [测试覆盖](/help/tests/)

117 项自动化测试验证了完整的 IEC 61131-3 语言特性集、
全部 132 个标准库模块以及多任务线程系统。

### [开源哲学](/help/open-source/)

开源背后的理念远超软件本身——它是一场解放知识、
民主化创新的运动。

---

## 入门

ForgeIEC 由两个组件组成：

1. **ForgeIEC 编辑器** (`forgeiec`) — 工作站上的开发环境
2. **ForgeIEC 守护进程** (`anvild`) — 目标 PLC 上的运行时系统

### 从 ForgeIEC APT 仓库安装

ForgeIEC 以签名的 Debian 仓库形式在 `apt.forgeiec.io` 上提供。
每个工作站或目标 PLC 只需设置一次：

```bash
# 导入签名密钥
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# 添加仓库源
# （Debian 12 "bookworm" 或 Debian 13 "trixie" — 根据您的系统选择）
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

然后使用标准包管理器安装任何 ForgeIEC 软件包：

```bash
# 编辑器（工作站）
sudo apt install forgeiec

# 守护进程（目标 PLC）
sudo apt install anvild
```

更新遵循正常的 `apt update && apt upgrade` 生命周期——
无需手动 `.deb` 文件。

### 支持的平台

| 组件     | 架构          | Debian 版本      |
|----------|---------------|------------------|
| 编辑器   | amd64, arm64  | bookworm, trixie |
| 守护进程 | amd64, arm64  | bookworm, trixie |
| Bridges  | amd64, arm64  | bookworm, trixie |
| Hearth   | amd64, arm64  | bookworm, trixie |

### 联系

如有问题：blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**文档随项目一起成长。**

blacksmith@forgeiec.io

</div>
