---
title: "总线配置"
summary: "用于工业现场总线配置的 PLCopen XML 架构"
---

## 命名空间

```
https://forgeiec.io/v2/bus-config
```

本架构描述了 ForgeIEC 对 PLCopen XML 格式的扩展，
用于在 `.forge` 项目文件中存储现场总线配置。
它使用 PLCopen TC6 定义的标准 `<addData>` 机制。

## 概述

总线配置定义了工厂的物理拓扑：
**段**（现场总线网络）包含**设备**，每个设备通过
总线绑定与项目的 I/O 变量关联。

```
.forge 项目
  +-- 段（现场总线网络）
  |     +-- 设备
  |           +-- 变量（通过地址池中的总线绑定）
  +-- 地址池（FAddressPool）
        +-- 变量：DI_1, %IX0.0, busBinding -> Maibeere
        +-- 变量：DO_1, %QX0.0, busBinding -> Maibeere
```

## XML 结构

总线配置作为 `<addData>` 存储在项目级别：

```xml
<project>
  <!-- 标准 PLCopen 内容 -->
  <types>...</types>
  <instances>...</instances>

  <!-- ForgeIEC 总线配置 -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="现场总线车间 1"
                    enabled="true"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    gateway=""
                    pollIntervalMs="0">

          <fi:device hostname="Maibeere"
                     ipAddress="192.168.24.25"
                     port="502"
                     slaveId="1"
                     anvilGroup="Maibeere"/>

          <fi:device hostname="Stachelbeere"
                     ipAddress="192.168.24.26"
                     port="502"
                     slaveId="1"
                     anvilGroup="Stachelbeere"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

## 元素

### `fi:busConfig`

根元素。包含一个或多个 `fi:segment` 元素。

| 属性 | 必需 | 描述 |
|------|------|------|
| `xmlns:fi` | 是 | 命名空间：`https://forgeiec.io/v2` |

### `fi:segment`

一个现场总线段（物理网络）。

| 属性 | 必需 | 类型 | 描述 |
|------|------|------|------|
| `id` | 是 | UUID | 唯一段标识符 |
| `protocol` | 是 | String | 协议：`modbustcp`、`modbusrtu`、`ethercat`、`profibus` |
| `name` | 是 | String | 显示名称（用户自定义） |
| `enabled` | 否 | Bool | 段激活（`true`）或禁用（`false`）。默认：`true` |
| `interface` | 否 | String | 网络接口（如 `eth0`、`/dev/ttyUSB0`） |
| `bindAddress` | 否 | String | 接口的 IP/CIDR（如 `192.168.24.100/24`） |
| `gateway` | 否 | String | 网关地址（空 = 无网关） |
| `pollIntervalMs` | 否 | Int | 轮询间隔（毫秒）（`0` = 尽可能快） |

### `fi:device`

段内的一个设备。

| 属性 | 必需 | 类型 | 描述 |
|------|------|------|------|
| `hostname` | 是 | String | 设备名称（用作设备 ID） |
| `ipAddress` | 否 | String | IP 地址（Modbus TCP） |
| `port` | 否 | Int | TCP 端口（默认：`502`） |
| `slaveId` | 否 | Int | Modbus 从站 ID |
| `anvilGroup` | 否 | String | Anvil IPC 组（零拷贝传输） |

## 变量到设备的绑定

I/O 变量**不在** `fi:device` 元素中列出。
地址池中的每个变量都带有一个 `busBinding` 属性，
指向设备的 `hostname`：

```
FLocatedVariable
  name: "DI_1"
  address: "%IX0.0"
  anvilGroup: "Maibeere"
  busBinding:
    deviceId: "Maibeere"
    modbusAddress: 0
    count: 1
```

## IEC 地址分配

绑定变量的 IEC 地址由物理拓扑决定：

```
段基地址 + 设备偏移 + 寄存器位置
```

| 地址范围 | 含义 | 来源 |
|----------|------|------|
| `%IX` / `%IW` / `%ID` | 物理输入 | 总线绑定 |
| `%QX` / `%QW` / `%QD` | 物理输出 | 总线绑定 |
| `%MX` / `%MW` / `%MD` | 标记（无物理 I/O） | 池分配器 |

## 支持的协议

| 协议 | `protocol` 值 | 介质 | 桥接守护进程 |
|------|--------------|------|-------------|
| Modbus TCP | `modbustcp` | 以太网 | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485（串行） | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | 以太网（实时） | `tongs-ethercat` |
| Profibus DP | `profibus` | 串行（现场总线） | `tongs-profibus` |

## 兼容性

`handleUnknown="discard"` 属性确保不了解 ForgeIEC 的
PLCopen 工具可以安全地忽略总线配置而不产生错误。
反之，ForgeIEC 读取其他供应商的未知 `<addData>` 块
并在保存时保留它们。

---

<div style="text-align:center; padding: 2rem;">

**ForgeIEC 总线配置 — 离线可用、PLCopen 兼容、无冗余。**

blacksmith@forgeiec.io

</div>
