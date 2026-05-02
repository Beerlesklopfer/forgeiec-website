---
title: "バスデバイス"
summary: "バスセグメント内のデバイスの設定 (Modbus スレーブ、EtherCAT スレーブなど)"
---

## 概要

**バスデバイス** は **セグメント内の単一のデバイス** です。典型的には
Modbus TCP スレーブ (I/O ブロック、ドライブ)、EtherCAT スレーブ (サーボ
軸、I/O カプラ)、Profibus DP スレーブ、または EtherNet-IP アダプタです。
各デバイスについて、担当するブリッジは 1 つの論理接続を維持し、設定
されたレジスタをポーリングして、Anvil IPC グループを介して PLC ランタイム
にデータを発行します。

デバイスは **モジュラー** にすることができます。バスカプラ (スロット 0)
が 1〜N 個の I/O モジュールをスロット 1〜N に保持します。拡張スロット
を持たないコンパクトデバイスでは `modules` リストが空になり、変数は
スロット 0 に直接配置されます。

## デバイスのフィールド

構造体定義は `editor/include/model/FBusSegmentConfig.h` (セグメントの
隣) にあります。デバイスは `.forge` プロジェクトで `<fi:segment>` 内の
`<fi:device>` として永続化されます ([バス設定](../) を参照)。

### 識別子 + アドレス指定

| フィールド | 型 | 意味 |
|---|---|---|
| `deviceId` | UUID | 安定した主キー — 作成時に自動生成。ホスト名のリネームや IP 変更を経ても維持され、すべての変数バインディングを安定させます。 |
| `hostname` | string | ユーザーに見えるラベル (`"Maibeere"`, `"Stachelbeere"`)。DHCP セーフですが、明示的に主キーでは **ありません**。 |
| `ipAddress` | string (IP) | IP アドレス (Modbus TCP / EtherNet-IP)。IP を持たないデバイスでは空 (EtherCAT スレーブはバス位置で自身を識別します)。 |
| `port` | int | TCP ポート。デフォルト `502` (Modbus TCP)。 |
| `slaveId` | int | Modbus スレーブ ID (1..247)。TCP では通常 `1`。 |
| `anvilGroup` | string | ブリッジと PLC ランタイム間のゼロコピー転送用 Anvil IPC グループ。慣例: `hostname` と同じ名前。 |
| `catalogRef` | string | デバイスを記述する FDD カタログエントリへの任意参照 (`"WAGO-750-352"`)。 |
| `description` | string | 自由記述テキスト (`"Bewaesserungsventil Sued"`)。 |

### モジュール (スロット)

| フィールド | 型 | 意味 |
|---|---|---|
| `modules` | list of `FBusModuleConfig` | デバイスの I/O モジュール。スロット 0 = カプラ / コンパクトデバイス、スロット 1〜N = 拡張モジュール。モジュールごとに `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`。 |

### デバイスごとのオーバーライド

これらのフィールドは — **このデバイス** に対してのみ — セグメントの
対応する値をオーバーライドします。`0` または空文字列は *セグメントから
継承* を意味します。プロパティパネルでは *Advanced Overrides* ブロック
の下に配置され、通常は折りたたまれています。

| フィールド | 型 | 意味 |
|---|---|---|
| `mac` | string `AA:BB:CC:DD:EE:FF` | 静的 ARP / 同一性チェック用 MAC アドレス。DHCP デバイスにおける IP 盗用に対する保護。 |
| `endianness` | enum | マルチレジスタ値のワード/バイト順: `"ABCD"` (ビッグエンディアン、IEC デフォルト)、`"DCBA"` (ワードスワップ)、`"BADC"` (バイトスワップ)、`"CDAB"` (バイト + ワードスワップ)。空 = セグメントから継承。 |
| `timeoutOverrideMs` | int (ms) | デバイスごとのタイムアウト。`0` = セグメントのタイムアウトを使用。 |
| `retryCount` | int | リクエストごとの再試行回数。`0` = セグメントデフォルト。 |
| `connectionMode` | enum | `"always"` (サイクル間で TCP を開いたまま) または `"on_demand"` (トランザクションごとに再接続)。空 = セグメント / ブリッジのデフォルト。 |
| `gatewayOverride` | string (IP) | デバイスがバインド NIC とは異なるサブネットにある場合のデバイスごとのゲートウェイ。 |

### デバイス固有の設定

`settings` マップ (key/value) には、このデバイスまたはそのデバイスタイプ
にのみ意味のある値が格納されます。たとえばドライブのしきい値や優先
ファンクションコードなどです。

## 編集フロー

| 操作 | 効果 |
|---|---|
| **シングルクリック** (デバイスノード上で) | `FPropertiesPanel` がすべてのフィールドをインラインエディタとして表示します。General ブロック (hostname, IP, port, slave ID, Anvil group)、Override ブロック (MAC, timeout, retries, endianness, connection mode, gateway override, description)、ステータステーブルが含まれます。 |
| **ダブルクリック** (デバイスノード上で) | モーダルな `FBusDeviceDialog` を同じフィールドセットで開きます。編集モードでは「Import from catalog」ボタンがロックされ、後からの FDD インポートが既存の I/O 変数バインディングを暗黙のうちに上書きしないようにします。 |

## ステータス変数 (読み取り専用)

実行時に各デバイスはステータス構造を発行し、デーモンはそれを gRPC
ステータスストリームを介して送信します。これらの値はプロパティパネル
で **読み取り専用テーブル** として表示され、UI からは **編集できません** —
ブリッジが書き込みます。ST コードからは引き続き
`anvil.<seg>.<dev>.Status.*` の修飾パスとしてアクセスできます:

| ステータス変数 | 型 | 意味 |
|---|---|---|
| `xOnline` | `BOOL` | デバイスが現在到達可能 (最後のリクエストに応答あり)。 |
| `eState` | `INT` | 状態 enum: 0=オフライン、1=接続中、2=オンライン、3=エラー。 |
| `wErrorCount` | `WORD` | ブリッジ起動以降の失敗リクエスト数のカウンタ。 |
| `sLastErrorMsg` | `STRING` | 最後のエラーメッセージ (タイムアウト、Modbus 例外など)。 |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## 例: 2 スロット構成の WAGO 750 バスカプラ

スロット 1 に 8-DI モジュール (750-430)、スロット 2 に 8-DO モジュール
(750-530) を持つ Modbus TCP バスカプラ 750-352:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

8 個の入力はアドレスプール内に `%IX0.0..%IX0.7` として、`deviceId="0e5d5537-..."`、
`moduleSlot=1`、`modbusAddress=0..7` で現れます。8 個の出力も同様に
`moduleSlot=2` で現れます。

## 関連項目

* [バスセグメント](../segments/) — デバイスが存在するネットワーク。
* [バス設定 — スキーマ概要](../) — XML 永続化。
* [プロジェクトファイル形式](../../file-format/) — アドレスプールおよび
  変数とデバイスのバインディング。
