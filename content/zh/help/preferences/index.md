---
title: "首选项"
summary: "中央编辑器配置对话框：编辑器、运行时、PLC、AI 助手"
---

## 概述

**首选项对话框**是所有编辑器全局设置的统一入口 ——
所有*不*属于打开项目，而是配置编辑器本身、与运行时
的连接以及上传后行为的内容。

通过 **`Edit > Preferences...`** 打开对话框（某些主题
将其放在 `Tools > Preferences...` 下）。当对话框获得焦点时，
按 **F1** 即可直接打开此页面。

```
Preferences
+-- Editor          (font, tab width, line numbers)
+-- Runtime         (anvild host/port, Anvil debug, network scanner)
+-- PLC             (build mode, auto-start, persist, monitoring)
+-- AI Assistant    (LLM endpoint, tokens, temperature)
```

## 编辑器

控制 ST 代码编辑器及所有其他文本输入字段中文本的显示方式。

| 字段 | 含义 |
|---|---|
| **Font**         | 字体族。已预过滤为等宽字体（推荐：`JetBrains Mono`、`Cascadia Code`、`Consolas`）。 |
| **Font size**    | 字号（磅）。默认 `10`。 |
| **Tab width**    | 每个制表位的空格数。默认 `4`。 |
| **Show line numbers** | 在代码编辑器的边栏中显示连续的行号。 |

## 运行时

与 **anvild** 守护进程的连接以及 IPC 诊断。

| 字段 | 含义 |
|---|---|
| **Host**         | PLC 主机名或 IP。默认 `localhost`。 |
| **Port**         | anvild 的 gRPC 端口。默认 `50051`。 |
| **User**         | 用于令牌认证的用户名。 |
| **Anvil Debug**  | IPC 诊断级别（`Off`、`Errors only`、`Verbose`）。在 anvild 日志中增加额外统计信息 —— 有助于在生产环境中排查 Iceoryx 主题漂移。 |

此外：**Auto-Connect on start** 会在编辑器启动时自动连接到
最近一次成功连接的 anvild —— 在专用工程笔记本上很方便。

同一选项卡上的 **Network Scanner** 块会扫描局域网中的 Modbus
TCP 设备（端口 502）和 ForgeIEC 运行时（端口 50051），
并将命中结果插入总线配置。

## PLC

控制**上传**到 PLC 后的行为。

| 字段 | 含义 |
|---|---|
| **Compile Mode** | `Development`（启用实时监视和强制）或 `Production`（精简二进制，无调试桥接 —— 安全边界）。 |
| **PLC autostart**| 在成功上传后自动启动 PLC 运行时，跳过确认对话框。 |
| **Persist enabled** | 启用 `VAR_PERSIST`/`RETAIN` 变量到 `/var/lib/anvil/persistent.dat` 的周期性持久化。值在运行时重启后保留。 |
| **Persist polling interval** | 自动保存之间的间隔秒数（默认 `5 s`）。 |
| **Monitor history** | 示波器记录器中每个变量的样本数（默认 `1000`）。 |
| **Monitor interval**| 实时监视的采样间隔（毫秒，默认 `100 ms`）。 |

## 库

编辑器资源与 PLC 端库路径之间标准库的同步行为 ——
完整漂移模型见[库](../library/)。两种模式：

  - **Auto-Push 关闭**（默认）—— 连接时若检测到漂移，
    编辑器仅在 Output 面板记录提示。推送通过
    `Tools > Sync Library` 手动触发。
  - **Auto-Push 开启** —— 每次检测到漂移时编辑器会
    自动推送本地库版本。适用于单一程序员的工作场景。

## AI 助手

针对本地 OpenAI 兼容 LLM 服务器（LM Studio、Ollama、
llama.cpp、vLLM）的可选代码补全。

| 字段 | 含义 |
|---|---|
| **Enable AI Assistant** | 切换内联补全。 |
| **API Endpoint**        | OpenAI 兼容端点，例如 `http://localhost:1234/v1`。 |
| **Max Tokens**          | 每次请求的响应限制。默认 `2048`。 |
| **Temperature**         | `Precise (0.1)`、`Balanced (0.3)`、`Creative (0.7)`、`Wild (1.0)`。 |

## UX 状态（自动持久化）

以下字段在后台保存，**不**经过首选项对话框，
以便编辑器重新打开时保持您离开时的精确状态：

  - 窗口几何 + 窗口状态（`windowGeometry`、`windowState`）
  - 分割器和表头位置（`splitterState`、`headerState`）
  - Output 面板高度（`outputPanelHeight`）
  - 最近打开的项目（`lastProject`）和最近文件列表
  - 会话状态：打开的 POU 选项卡、当前选项卡、每个 POU
    的光标和滚动位置

## 设置存储

设置通过 Qt 的 `QSettings` 存储，依平台而定：

| 平台 | 路径 |
|---|---|
| **Windows** | 注册表：`HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

删除该文件 / 注册表键会将所有设置重置为默认值 ——
在升级失败后非常有用。

## 计划中的扩展

待办（cluster R 第三阶段）：Output 面板将获得自己的严重程度
颜色（错误红、警告黄、信息白）以及可配置字号。届时这两个
选项将出现在新的 `Output` 选项卡上。

## 相关主题

  - [库](../library/) —— 编辑器与运行时之间的同步行为。
  - [总线配置](../bus-config/) —— 项目作用域的设置不在此处，
    而是位于总线段 / 设备本身。
