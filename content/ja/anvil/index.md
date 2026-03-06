---
title: "Anvil"
summary: "お客様のデータは私たちのアンビルで鍛造されます"
---

## アンビル：鍛冶場の心臓部

すべての鍛冶場において、アンビル（金床）は中心的な存在です——
ここで金属が形作られ、焼き入れされ、精錬されます。**Anvil** は
PLCランタイムとフィールドバスブリッジの間の中間層です。
プロセスデータはここで鍛造されます：受信、変換、そして適切な
受信者への配信。

Anvilは内部的に **IceOryx2** 上に構築されています——プロセス間通信のための
ゼロコピー共有メモリフレームワークです。シリアライゼーションなし、
コピーなし、妥協なし。

---

## アーキテクチャ

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ PLCプログラム │◄───────►│  forgeiecd  │◄───────►│  Modbusブリッジ   │──► フィールド機器
│  (IECコード)  │  gRPC   │ (デーモン)  │  Anvil  │  EtherCATブリッジ  │──► ドライブ
│              │         │            │ IceOryx2│  Profibusブリッジ   │──► センサー
└──────────────┘         └────────────┘         │  OPC-UAブリッジ    │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         ゼロコピー IPC
                         共有メモリ
```

`forgeiecd` とプロトコルブリッジ間のデータ交換は **Anvil** を通じて行われます——
IceOryx2共有メモリに基づく高性能IPCチャネルです。
各セグメントに独自の通信チャネルが割り当てられます。

---

## なぜAnvilか？

### マイクロ秒レベルの遅延

従来のIPCメカニズム（パイプ、ソケット、メッセージキュー）はプロセス間で
データをコピーします。Anvilはすべてのコピーを排除します。データは共有メモリ
に常駐し、受信側が直接読み取ります。

| 方式 | 典型的な遅延 | コピー回数 |
|------|------------|-----------|
| TCPソケット | 50–200 マイクロ秒 | 2–4 |
| Unixソケット | 10–50 マイクロ秒 | 2 |
| **Anvil (IceOryx2)** | **< 1 マイクロ秒** | **0** |

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
コンパイラがIceOryx2バインディングを自動生成します。

---

## サポートされるプロトコル

| プロトコル | ブリッジ | ステータス |
|-----------|---------|----------|
| **Modbus TCP** | `forgeiec-modbustcp` | 利用可能 |
| **Modbus RTU** | `forgeiec-modbusrtu` | 利用可能 |
| **EtherCAT** | `forgeiec-ethercat` | 開発中 |
| **Profibus DP** | `forgeiec-profibus` | 開発中 |
| **OPC-UA** | `forgeiec-opcua` | 計画中 |

各ブリッジは独立したプロセスとして動作します。`forgeiecd` がブリッジの
起動、監視、自動再起動を管理します。

---

<div style="text-align:center; padding: 2rem;">

**Anvil——データが制御コマンドに鍛造される場所。**

blacksmith@forgeiec.io

</div>
