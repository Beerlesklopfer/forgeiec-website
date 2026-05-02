---
title: "プロパティパネル"
summary: "プロジェクトツリーで選択されたバス要素のインラインエディタ"
---

## 概要

**Properties パネル** は、エディタのメインウィンドウの右側の詳細ビュー
です。**プロジェクトツリーで現在選択されている要素のすべてのフィールド**
を表示し、それらのフィールドをインラインで編集可能にします — 編集ごと
にモーダルダイアログを開く必要はありません。

```
Project tree                          Properties panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- click   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

ツリーノードへの **シングルクリック** は、即座に対応するフィールド
リストをレンダリングします — **ダブルクリック** はさらに、まったく同じ
フィールドセットを持つモーダル設定ダイアログ ([バス設定](../bus-config/))
を開きます。

このパネルは `QScrollArea` でラップされ、垂直方向にスクロールします。
FDD 拡張を持つデバイスにステータステーブルを加えると 40 個以上の
フィールドに容易に到達するため、ドックが狭い場合でもすべてに到達可能
である必要があります。

## バスセグメント

バスセグメントが選択されている場合、パネルには以下が表示されます:

| フィールド | 意味 |
|---|---|
| **Name** | プロジェクトツリーの表示名。 |
| **Protocol** | `modbustcp`, `modbusrtu`, `ethercat`, `profibus`, `ethernetip`。 |
| **Interface** | ブリッジがバインドするネットワークインタフェース (`eth0`, `eth1`, …)。 |
| **Bind Address** | CIDR 表記 (例: `192.168.1.10/24`)。検証されます。 |
| **Gateway** | ブリッジプロセスのデフォルトゲートウェイ。 |
| **Poll Interval** | ブリッジがデバイスをポーリングする周期 (`ms`)。 |
| **Enabled** | ブリッジサブプロセスがアクティブかどうか。 |

### Advanced Network (すべてオプション)

`FSegmentDialog` の同じグループをミラーリングし、OS / ブリッジのデフォ
ルトをオーバーライドします:

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count** (TCP ハートビート)
  - **Max Connections** (`0` = 無制限)
  - **VLAN ID** (`0` = タグなし)

### プロトコル固有

| プロトコル | フィールド |
|---|---|
| `modbustcp`  | `Port` (デフォルト `502`)、`Timeout` (`ms`、デフォルト `2000`)。 |
| `modbusrtu`  | `Serial Port` (例: `/dev/ttyUSB0`)、`Baud Rate`、`Parity` (`none`/`even`/`odd`)。 |
| `profibus`   | `Serial Port`、`Baud Rate` (最大 12 Mbit/s)、`Master Address` (0..126)。 |

### ロギング

  - **Log Level** — `off` / `error` / `warn` / `info` / `debug`。
  - **Log File** — 例: `/var/log/forgeiec/segment.log`。空 = 標準出力。

## バスデバイス

| フィールド | 意味 |
|---|---|
| **Hostname** | DNS または表示名。 |
| **IP Address** | デバイスの IPv4。 |
| **Port** | スレーブの Modbus ポート (デフォルト `502`)。 |
| **Slave ID** | Modbus ユニット ID (0..247)。 |
| **Anvil Group** | Anvil IPC グループ名 — 自動生成される `AnvilVarList` の名前でもあります。これをリネームすると、GVL タグ、AnvilVarList、`anvilGroup = oldGroup` のすべてのプール変数が同期的にリネームされます。 |

### Advanced overrides (すべてオプション、空 = セグメントから継承)

  - **MAC Address** — `AA:BB:CC:DD:EE:FF`。検証されます。
  - **Endianness** — `ABCD` / `DCBA` / `BADC` / `CDAB`。
  - **Timeout** (`ms`)。`0` = セグメントから継承。
  - **Retry Count**。`0` = セグメントから継承。
  - **Connection Mode** — `always connected` または `on demand`。
  - **Gateway (override)** — デバイスが異なるサブネットにある場合のみ。
  - **Description** — 自由記述テキスト (例: `South irrigation valve`)。

### ステータス変数 (読み取り専用)

各デバイスは共通の障害モデルを自動的に公開します — Anvil 経由で読み取り
専用ステータストピックとして発行される 7 つの暗黙フィールド:

| 名前 | IEC 型 | 意味 |
|---|---|---|
| `xOnline`              | `BOOL`         | `eState = Online` または `Degraded` のときに TRUE。 |
| `eState`               | `eDeviceState` | 現在の障害状態。 |
| `wErrorCount`          | `UDINT`        | ブリッジ起動以降のエラー総数。 |
| `wConsecutiveFailures` | `UDINT`        | 最後の `Online` 以降の障害数 (`Online` でリセット)。 |
| `wLastErrorCode`       | `UINT`         | `0` = なし、`1..99` 共通、`100+` プロトコル固有。 |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8、ゼロパディング。 |
| `tLastTransition`      | `ULINT`        | 最後の状態遷移の Unix 時刻 (ms)。 |

デバイスが `catalogRef` 経由で **FDD** (フィールドデバイス記述) に
バインドされている場合、ステータステーブルには FDD 定義の拡張も追加で
リストされ、`Source` カラムに `FDD +<offset>` でマークされます。

ST コードでは、すべてのステータス変数に `anvil.<seg>.<dev>.Status.*`
として到達できます:

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## バスモジュール

バスモジュールは、デバイス内の I/O スライスです。パネルには以下が表示
されます:

### メタデータ

  - **Module** (表示名または `catalogRef`)
  - **Slot** (デバイス内のスロットインデックス)
  - **Catalog** (FDD 参照、例: `Beckhoff.EL2008`)
  - **Base Addr** (IEC ベースオフセット)

### IO 変数テーブル

`busBinding.deviceId` と `busBinding.moduleSlot` がこのモジュールと一致
するすべてのプール変数をリストします。カラム:

| カラム | 内容 |
|---|---|
| **Name** | プール名 (編集可能、例: `Motor_Run`)。 |
| **Type** | IEC 型 (編集可能、例: `BOOL`, `INT`)。 |
| **Address** | IEC アドレス (`%IX0.0`、読み取り専用)。 |
| **Bus Addr** | Modbus レジスタオフセット (読み取り専用)。 |
| **Dir** | `in` または `out` (読み取り専用)。 |

ソート順: 入力が出力の前、その後バスアドレスの昇順。

## 編集動作

パネル内の各編集はモデルに対して直接実行されます:

  1. ウィジェット上での編集 (`editingFinished` / `valueChanged` /
     `toggled`)。
  2. モデルフィールドが更新されます (`seg->name = ...`)。
  3. `project->markDirty()` が dirty フラグを立てます。
  4. `busConfigEdited` シグナルが発行されます。
  5. 必要に応じて、メインウィンドウがプロジェクトツリーラベルを更新
     します。

明示的な `Apply` も `Cancel` も **ありません** — 編集は即座に有効に
なります。プロジェクトツリーでの `Ctrl+Z` (アンドゥ) で最後の編集を
取り消せます。

## 関連項目

  - [バス設定](../bus-config/) — 同じフィールドセットを持つモーダル
    ダイアログ。編集量の多いパワーユーザー向け。
  - [Variables パネル](../variables/) — `IO variables` テーブルを供給
    するプール。
