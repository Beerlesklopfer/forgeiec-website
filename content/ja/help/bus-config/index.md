---
title: "バス設定"
summary: "産業用フィールドバス設定のための PLCopen XML スキーマ"
---

## 名前空間

```
https://forgeiec.io/v2/bus-config
```

このスキーマは、`.forge` プロジェクトファイル内にフィールドバス設定を
保存するための PLCopen XML フォーマットの ForgeIEC 拡張を定義します。
PLCopen TC6 で定義された標準準拠の `<addData>` メカニズムを使用します。

## 概要

バス設定はプラントの物理トポロジーを定義します：
**セグメント**（フィールドバスネットワーク）は**デバイス**を含み、
各デバイスはバスバインディングを通じてプロジェクトの I/O 変数に
リンクされます。

```
.forge プロジェクト
  +-- セグメント（フィールドバスネットワーク）
  |     +-- デバイス
  |           +-- 変数（アドレスプール内のバスバインディング経由）
  +-- アドレスプール（FAddressPool）
        +-- 変数：DI_1, %IX0.0, busBinding -> Maibeere
        +-- 変数：DO_1, %QX0.0, busBinding -> Maibeere
```

## XML 構造

バス設定はプロジェクトレベルの `<addData>` として保存されます：

```xml
<project>
  <!-- 標準 PLCopen コンテンツ -->
  <types>...</types>
  <instances>...</instances>

  <!-- ForgeIEC バス設定 -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="フィールドバス ホール 1"
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

## 要素

### `fi:busConfig`

ルート要素。1つ以上の `fi:segment` 要素を含みます。

| 属性 | 必須 | 説明 |
|------|------|------|
| `xmlns:fi` | はい | 名前空間：`https://forgeiec.io/v2` |

### `fi:segment`

フィールドバスセグメント（物理ネットワーク）。

| 属性 | 必須 | 型 | 説明 |
|------|------|-----|------|
| `id` | はい | UUID | 一意のセグメント識別子 |
| `protocol` | はい | String | プロトコル：`modbustcp`、`modbusrtu`、`ethercat`、`profibus` |
| `name` | はい | String | 表示名（自由設定） |
| `enabled` | いいえ | Bool | セグメント有効（`true`）または無効（`false`）。デフォルト：`true` |
| `interface` | いいえ | String | ネットワークインターフェース（例：`eth0`、`/dev/ttyUSB0`） |
| `bindAddress` | いいえ | String | インターフェースの IP/CIDR（例：`192.168.24.100/24`） |
| `gateway` | いいえ | String | ゲートウェイアドレス（空 = ゲートウェイなし） |
| `pollIntervalMs` | いいえ | Int | ポーリング間隔（ミリ秒）（`0` = できるだけ速く） |

### `fi:device`

セグメント内のデバイス。

| 属性 | 必須 | 型 | 説明 |
|------|------|-----|------|
| `hostname` | はい | String | デバイス名（デバイス ID として使用） |
| `ipAddress` | いいえ | String | IP アドレス（Modbus TCP） |
| `port` | いいえ | Int | TCP ポート（デフォルト：`502`） |
| `slaveId` | いいえ | Int | Modbus スレーブ ID |
| `anvilGroup` | いいえ | String | ゼロコピー転送用 Anvil IPC グループ |

## 変数とデバイスのバインディング

I/O 変数は `fi:device` 要素内に**リストされません**。
代わりに、アドレスプール内の各変数がデバイスの `hostname` を
指す `busBinding` 属性を持ちます：

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

## IEC アドレス割り当て

バインドされた変数の IEC アドレスは物理トポロジーから導出されます：

```
セグメントベース + デバイスオフセット + レジスタ位置
```

| アドレス範囲 | 意味 | ソース |
|-------------|------|--------|
| `%IX` / `%IW` / `%ID` | 物理入力 | バスバインディング |
| `%QX` / `%QW` / `%QD` | 物理出力 | バスバインディング |
| `%MX` / `%MW` / `%MD` | マーカー（物理 I/O なし） | プールアロケータ |

## サポートされるプロトコル

| プロトコル | `protocol` 値 | メディア | ブリッジデーモン |
|-----------|--------------|---------|----------------|
| Modbus TCP | `modbustcp` | イーサネット | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485（シリアル） | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | イーサネット（リアルタイム） | `tongs-ethercat` |
| Profibus DP | `profibus` | シリアル（フィールドバス） | `tongs-profibus` |

## 互換性

`handleUnknown="discard"` 属性により、ForgeIEC を知らない
PLCopen 準拠ツールはバス設定をエラーなく安全に無視できます。
逆に、ForgeIEC は他のベンダーの未知の `<addData>` ブロックを
読み取り、保存時にそれらを保持します。

---

<div style="text-align:center; padding: 2rem;">

**ForgeIEC バス設定 — オフライン対応、PLCopen 準拠、冗長性なし。**

blacksmith@forgeiec.io

</div>
