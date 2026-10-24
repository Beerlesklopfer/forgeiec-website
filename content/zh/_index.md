---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# 为工业锻造。

**工业级 IEC 61131-3 开发环境。开源。**

[联系我们](mailto:blacksmith@forgeiec.io)

</div>

---

## 我们在做什么

ForgeIEC 是一个功能完整的 IEC 61131-3 工业自动化开发环境——
五种 IEC 语言、工业总线系统、实时调试。

以与成熟商业系统平起平坐为目标而开发。每个功能在发布前
均通过文档化的测试验证。

---

## 为什么选择开源

工业自动化是一项关键技术。但专业工具的使用受到许可费用和
专有系统的限制。ForgeIEC 让自动化的价值惠及每一个人——
无供应商锁定，无许可费用。

作为开源项目，ForgeIEC 属于社区。

---

## 快速开始

```bash
# 导入签名密钥（仅需一次）
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# 添加软件源
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# 安装编辑器和运行时
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

以上以 Debian 13 (trixie) 为例。Debian 12 (bookworm) 或 Ubuntu 24.04 (noble) 请替换两处 `trixie`。所有发行版、RPM 及其他软件包：[下载](/download/)。

---

<div style="text-align:center; padding: 2rem;">

**工业级版本就绪后，我们将发布详细信息。**

blacksmith@forgeiec.io

</div>
