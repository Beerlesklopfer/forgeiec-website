---
title: "バスセグメント"
summary: "フィールドバスセグメント (1 つのインタフェース上の物理ネットワーク) の設定"
---

## 概要

**バスセグメント** は **PLC ターゲットの 1 つのインタフェース上にある
1 つの物理ネットワーク** を記述します。典型的には、Modbus TCP /
EtherCAT / EtherNet-IP 用のイーサネットポート (`eth0`, `enp3s0`)、
または Modbus RTU / Profibus DP 用のシリアルポート (`/dev/ttyUSB0`)
です。各セグメントについて、`anvild` デーモンは **正確に 1 つのブリッジ
プロセス** (`tongs-modbustcp`, `tongs-ethercat`, ...) を起動し、その
セグメント内のすべてのデバイスとのトラフィックを処理します。

プロジェクトには任意の数のセグメントを保持できます。各セグメントは
独自のプロトコル、独自のインタフェース、独自のポーリング周期を持ちます。
たとえば、高速な EtherCAT 軸コントローラ (`eth1`、1 ms) と低速な Modbus
TCP センサポーラ (`eth0`、100 ms) を、同じプロジェクト内で並行して
動作させることができます。

## セグメントのフィールド

構造体定義は `editor/include/model/FBusSegmentConfig.h` にあります。
セグメントは `.forge` プロジェクトで `<fi:busConfig>` 内の
`<fi:segment>` として永続化されます ([バス設定](../) を参照)。

### 識別子 + プロトコル

| フィールド | 型 | 意味 |
|---|---|---|
| `segmentId` | UUID | 安定した主キー — 作成時に自動生成され、編集不可。リネーム、プロトコル変更、IP 変更を経ても維持されます。 |
| `protocol` | enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`。どのブリッジデーモンが起動されるかを決定します。 |
| `name` | string | ユーザーラベル (例: `"Fieldbus Hall 1"`)。自由形式で、ツリーやログに表示されます。 |
| `enabled` | bool | オン/オフスイッチ。`false` = ブリッジは起動されず、デバイスはオフラインのまま。デフォルト: `true`。 |

### インタフェース + ルーティング

| フィールド | 型 | 意味 |
|---|---|---|
| `interface` | string | ネットワークインタフェース (`eth0`, `enp3s0`, `/dev/ttyUSB0`)。ブリッジから socket / serial API に渡されます。 |
| `bindAddress` | string (IP/CIDR) | 発信 TCP 接続のソース IP (例: `192.168.24.100/24`)。空 = OS がインタフェースの最初の IP を選択します。 |
| `gateway` | string (IP) | ローカルサブネットを離れるパケットのデフォルトゲートウェイ。空 = ゲートウェイなし。 |
| `pollIntervalMs` | int (ms) | ブリッジのポーリング間隔。`0` = 可能な限り高速 (ビジーループ / リアルタイム)。典型値: Modbus TCP は `100`、EtherCAT は `0`。 |

### ネットワーク設定 (高度)

これらのフィールドはネットワーク設定スプリントで追加され、OS のデフォ
ルトでは不十分なケースをカバーします。典型的には、スレーブごとの多数
の並列 TCP 接続、NAT 越しの長時間 TCP セッション、または単一 NIC 上の
複数サブネットなどです。

| フィールド | 型 | 意味 |
|---|---|---|
| `subnetCidr` | string (CIDR) | セグメントのローカルサブネット (例: `192.168.24.0/24`)。バインド NIC が複数のネットワークを持つ場合に、デバイスごとのゲートウェイオーバーライドを正しくルーティングできるようにします。 |
| `sourcePortRange` | string `"min-max"` | 発信接続用 TCP ソースポートプール (例: `30000-39999`)。空 = OS が ephemeral 範囲から選択します。同一スレーブへの多数の並列接続が必要な場合に重要です (ソースポートごとに 1 接続)。 |
| `keepAliveIdleSec` | int (s) | 最初の TCP keep-alive プローブが送信されるまでのアイドル秒数。`0` = OS デフォルト。 |
| `keepAliveIntervalSec` | int (s) | keep-alive プローブの間隔。`0` = OS デフォルト。 |
| `keepAliveCount` | int | 接続が切断と判定されるまでの失敗プローブ数。`0` = OS デフォルト。 |
| `maxConnections` | int | 接続プールの上限。`0` = 無制限。接続数に厳密な制限があるスレーブに対して有用です。 |
| `vlanId` | int (1..4094) | 発信フレーム用の 802.1Q VLAN タグ。`0` = タグなし。 |

### プロトコル固有の設定

`settings` マップ (key/value) には、特定のプロトコルにのみ意味のある
すべての値が含まれます。たとえば Modbus TCP では `port`, `timeout_ms`、
Modbus RTU では `serial_port`, `baud_rate`, `parity`, `stop_bits`、
Profibus では `master_address` など。`log_level` と `log_file` も同じ
マップ内にプロトコル非依存で保持されます。

## 編集フロー

バスツリーパネルでは両方の経路が等価です — どちらも同じフィールド
セットに対して動作し、同じセマンティクスの効果を持ちます:

| 操作 | 効果 |
|---|---|
| **シングルクリック** (セグメントノード上で) | `FPropertiesPanel` (デフォルトのドック位置: 右側) がすべてのフィールドをインラインエディタとして表示します。変更は `editingFinished` でプロジェクトに書き込まれ、プロジェクトを dirty とマークします。 |
| **ダブルクリック** (セグメントノード上で) | モーダルな `FSegmentDialog` を開きます。同じフィールドセットを *General* / *Modbus TCP* / *Advanced Network* / *Logging* にグループ化します。OK でコミット、Cancel で破棄。 |

## 例: Modbus TCP セグメント

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

このセグメントは `eth0` 上でソース IP `192.168.24.100` を使用して
`tongs-modbustcp` を起動し、すべてのデバイスを 100 ms ごとにポーリング
し、リクエストごとに最大 2000 ms の応答時間を許容します。それを超え
ると、ステータスストリームでタイムアウトエラーが発行されます。

## 関連項目

* [バス設定 — スキーマ概要](../) — XML 永続化と PLCopen `<addData>`
  メカニズム。
* [バスデバイス](../devices/) — セグメント内のデバイス。
* [プロジェクトファイル形式](../../file-format/) — `.forge` XML ルート。
