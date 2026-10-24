---
title: "下载"
summary: "ForgeIEC 全部组件 — APT 和 RPM 软件源、直接下载、源代码"
---

## ForgeIEC 组件一览

ForgeIEC 由多个组件组成。需要安装哪些组件取决于您的角色：

| 角色 | 组件 | 安装位置 |
|---|---|---|
| **PLC 程序员 / 用户** | `forgeiec-studio` | 工作站 |
| **调试工程师** | `forgeiec-anvil-server`（包含 `anvild`） | 目标 PLC |
| **HMI / OPC-UA 网关** | `forgeiec-bellows-server`（包含 `bellowsd`） | 目标 PLC 或独立主机 |
| **Modbus TCP** | 包含在 `forgeiec-anvil-server` 中 | 目标 PLC |
| **Profibus / EtherCAT / EthernetIP** | 同样包含在 `forgeiec-anvil-server` 中 | 目标 PLC |
| **操作面板** | `forgeiec-screen-wayland` 或 `-xorg` | 面板硬件 |

---

## 从软件包仓库安装

ForgeIEC 以签名的 Debian 仓库（`apt.forgeiec.io`）和签名的 RPM 仓库
（`rpm.forgeiec.io`）形式提供。每台工作站或目标 PLC 只需配置一次 —
请选择您的发行版：

{{< distro-install >}}

然后按需安装各个组件：

```bash
# 工作站
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # 设备描述文件（推荐）

# 目标 PLC
sudo apt install forgeiec-anvil-server    # PLC 运行时（anvild + 全部 tongs-*）
sudo apt install forgeiec-bellows-server  # HMI 网关（bellowsd）

# 操作面板
sudo apt install forgeiec-screen-wayland  # Wayland 下的 Kiosk 模式
sudo apt install forgeiec-screen-xorg     # X11 下的 Kiosk 模式
```

在 RPM 系统上，命令为 `sudo dnf install …`，软件包名称完全相同。

总线桥接程序（`tongs-modbustcp`、`tongs-ethercat`、`tongs-profibus`、
`tongs-ethernetip`）**不是**独立的软件包 — 它们包含在
`forgeiec-anvil-server` 中，并由 `anvild` 启动。

更新遵循标准的 `apt update && apt upgrade` 流程 — 无需手动处理 `.deb` 文件。

---

## 支持的平台

### Debian / Ubuntu（`apt.forgeiec.io`）

| 软件包 | 架构 | 发行版代号 |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | 与架构无关 | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

代号对应：`bullseye` = Debian 11，`bookworm` = Debian 12，
`trixie` = Debian 13，`jammy` = Ubuntu 22.04，`noble` = Ubuntu 24.04。

### Enterprise Linux / Fedora（`rpm.forgeiec.io`）

| 软件包 | 架构 | 发行版 |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9（`el9`）、Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9（`el9`）、Fedora 44 |

RPM 分发是新推出的，目前仅涵盖操作面板。ForgeIEC Studio 和运行时将在
其 RPM 打包稳定后跟进。

共有**两把不同的签名密钥**：apt 使用 `forgeiec.gpg`（ed25519），
rpm 使用 `forgeiec-rpm.asc`（RSA-4096）。这一区别并非表面差异 —
RHEL 9 自带的 `rpm` 4.16 的内置 PGP 解析器无法验证 ed25519。

RPM 端有意不提供 arm64：CI 的交叉编译流程依赖于 Enterprise Linux 上
不存在的 Debian 软件包。

ForgeIEC Studio 的 **Windows 版本**：正在准备中。在此之前，Studio 可在
Linux 上原生运行，或在 Windows 工作站上通过 WSL2 运行。

---

## 直接下载（发布压缩包）

如果您无法或不想使用软件包仓库 — 例如用于物理隔离（air gap）的工作站 —
可以从 Forgejo 获取单独的版本。**这些仓库不对外公开浏览**：请将您的 SSH
公钥发送至 blacksmith@forgeiec.io，我们会为您开通。之后您即可访问以下仓库：

- **ForgeIEC Studio 源代码**：`ForgeIEC/forgeiec-studio`
- **anvild + 桥接程序**：`ForgeIEC/anvil`
- **bellowsd**：`ForgeIEC/bellows`
- **网站源代码**：`ForgeIEC/forgeiec-website`

每个版本的签名 `.deb` 软件包和源代码压缩包都附在 Forgejo 的发布标签上。

---

## 从源代码构建

```bash
# 克隆仓库（含子模块）— 仅限 SSH，需先开通您的 SSH 公钥
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# 构建 Studio + 全部守护进程
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# 部署到本地系统
./deploy.sh all
```

前提条件：

- Debian 12/13 或 Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+（通过 rustup 安装）

---

## 演示项目

ForgeIEC Studio 自带的示例项目：

| 项目 | 用途 |
|---|---|
| `knight_rider.forge` | 用于 Bellows LED 的经典流水灯测试 |
| 更多即将推出 | … |

在 Studio 中通过 `File → Open Example` 打开。

---

## 后续步骤

- [ForgeIEC Studio 入门](/help/)
- [配置 AI 助手](/en/help/ai/)（英文）
- [总线配置](/help/bus-config/)
- [新闻 + 发布说明](/en/news/)（英文）
