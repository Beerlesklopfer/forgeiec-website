---
title: "Anvil Technology\u00ae"
summary: "お客様のデータは私たちのアンビルで鍛造されます"
---

## アンビル：鍛冶場の心臓部

すべての鍛冶場において、アンビル（金床）は中心的な存在です——
ここで金属が形作られ、焼き入れされ、精錬されます。**Anvil Technology\u00ae** は
PLCランタイムとフィールドバスブリッジの間の中間層です。
プロセスデータはここで鍛造されます：受信、変換、そして適切な
受信者への配信。

Anvilは内部的に独自のゼロコピー共有メモリトランスポートを使用しています——
プロセス間通信のためのものです。シリアライゼーションなし、
コピーなし、妥協なし。

---

## アーキテクチャ

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ PLCプログラム │◄───────►│  anvild  │◄───────►│  Modbusブリッジ   │──► フィールド機器
│  (IECコード)  │  gRPC   │ (デーモン)  │  Anvil  │  EtherCATブリッジ  │──► ドライブ
│              │         │            │ Anvil   │  Profibusブリッジ   │──► センサー
└──────────────┘         └────────────┘         │  OPC-UAブリッジ    │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         ゼロコピー IPC
                         共有メモリ
```

`anvild` とプロトコルブリッジ間のデータ交換は **Anvil Technology\u00ae** を通じて行われます——
ゼロコピー共有メモリに基づく高性能IPCチャネルです。
各セグメントに独自の通信チャネルが割り当てられます。

---

## なぜAnvil Technology\u00aeか？

### マイクロ秒レベルの遅延

従来のIPCメカニズム（パイプ、ソケット、メッセージキュー）はプロセス間で
データをコピーします。Anvilはすべてのコピーを排除します。データは共有メモリ
に常駐し、受信側が直接読み取ります。

| 方式 | 典型的な遅延 | コピー回数 |
|------|------------|-----------|
| TCPソケット | 50–200 マイクロ秒 | 2–4 |
| Unixソケット | 10–50 マイクロ秒 | 2 |
| **Anvil Technology\u00ae** | **< 1 マイクロ秒** | **0** |

### 産業グレード

- 決定論的動作——ホットパスでの動的メモリ割り当てなし
- ロックフリーアルゴリズム——ブロッキングなし、デッドロックなし
- Publish/Subscribeモデル——プロデューサーとコンシューマーの疎結合
- 自動ライフサイクル管理——ブリッジは監視され、クラッシュ時に自動再起動

### IECプログラムでのPUBLISH/SUBSCRIBE

```iec
VAR_GLOBAL PUBLISH 'Motors'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensors'
    Temperature AT %IW0   : INT;
    Pressure    AT %IW2   : INT;
END_VAR
```

PUBLISH/SUBSCRIBEキーワードはForgeIECによるIEC 61131-3標準の拡張です。
コンパイラがAnvilバインディングを自動生成します。

---

## サポートされるプロトコル

| プロトコル | ブリッジ | ステータス |
|-----------|---------|----------|
| **Modbus TCP** | `tongs-modbustcp` | 利用可能 |
| **Modbus RTU** | `tongs-modbusrtu` | 利用可能 |
| **EtherCAT** | `tongs-ethercat` | 開発中 |
| **Profibus DP** | `tongs-profibus` | 開発中 |
| **OPC-UA** | `tongs-opcua` | 計画中 |

各ブリッジは独立したプロセスとして動作します。`anvild` がブリッジの
起動、監視、自動再起動を管理します。

---

<div style="text-align:center; padding: 2rem;">

**Anvil Technology\u00ae——データが制御コマンドに鍛造される場所。**

blacksmith@forgeiec.io

</div>
