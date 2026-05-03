---
title: "在线帮助"
summary: "ForgeIEC 编辑器的上下文相关帮助入口"
---

## 在线帮助 — 这是什么？

在线帮助是 ForgeIEC 编辑器的上下文相关帮助层。在编辑器中按 **F1** 会
直接在浏览器中打开当前焦点元素（对话框、面板、变量表、代码生成
操作 ...）的帮助页面。

## URL 方案

所有帮助页面均采用统一的 URL 方案：

```
https://forgeiec.io/<语言>/help/<主题>/
```

- `<语言>` 跟随编辑器语言环境（de、en、fr、es、ja、tr、zh、ar）；
  当不存在本地化页面时默认为 `de`
- `<主题>` 是所有语言相同且不翻译的标识符

因此，您可以直接在浏览器中打开帮助页面，无需启动编辑器。

## 可用主题

### 编辑器与语言

- [Structured Text (ST)](/zh/help/st/) — ST 编辑器与语言基础
- [Instruction List (IL)](/zh/help/il/) — 基于累加器的 IEC 语言
- [Function Block Diagram (FBD)](/zh/help/fbd/) — 函数与功能块的图形化连接
- [Ladder Diagram (LD)](/zh/help/ld/) — 电路图比喻：电源线、触点、线圈
- [Sequential Function Chart (SFC)](/zh/help/sfc/) — 用于顺序控制的步骤-转移模型

### 模型与变量

- [变量管理](/zh/help/variables/) — Variables 面板作为 FAddressPool 的中心视图
- [库](/zh/help/library/) — IEC 61131-3 标准库 + ForgeIEC 扩展 + 用户自定义块
- [属性面板](/zh/help/properties-panel/) — 用于所选总线元素的内联编辑器
- [首选项](/zh/help/preferences/) — 中心配置对话框：编辑器、运行时、PLC、AI 助手

### 总线与硬件

- [总线配置](/zh/help/bus-config/) — 工业现场总线配置的 PLCopen XML 模式

### 通用

- [测试覆盖率](/zh/help/tests/) — 117 项 IEC 语言特性、标准块和多任务的自动化测试
- [开源理念](/zh/help/open-source/) — 背景

## 在编辑器中

- **F1** 在焦点元素上 → 上下文相关帮助页面
- **帮助 → 在线帮助** 在主菜单中 → 入口（本页）
- **帮助 → 关于 ForgeIEC** → 版本信息 + 许可证
