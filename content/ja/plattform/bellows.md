---
title: "Bellows"
description: "マシン間通信のための OPC UA ゲートウェイ"
weight: 3
---

## Bellows -- OPC UA ゲートウェイ

**開発中**

Bellows は ForgeIEC プラットフォームの OPC UA ゲートウェイです。鍛冶場のふいご
は火に空気を送ります -- Bellows はオートメーションシステムと IT インフラ
ストラクチャ間の通信を駆動します。

---

## マシン間通信

OPC UA（Open Platform Communications Unified Architecture）はインダストリー
4.0 の通信標準です。Bellows は PLC 変数を上位システムに公開する完全な OPC UA
サーバーを提供します。

### 想定されるユースケース

- **SCADA 統合** -- PLC を既存の監視システムに接続
- **M2M データ交換** -- PLC とサードパーティシステム間の直接通信
- **IT/OT ゲートウェイ** -- オートメーションネットワークと IT インフラ間のブリッジ
- **データアーカイブ** -- アーカイブのためのプロセスデータの提供

---

## 計画アーキテクチャ

Bellows は `anvild` デーモンによって管理される独立プロセスとして動作します。
プロセスデータは Anvil（ゼロコピー IPC）を通じて受信され、OPC UA プロトコル
を通じて公開されます。

```
PLC  --->  anvild  --->  Bellows (OPC UA サーバー)  --->  OPC UA クライアント
            Anvil IPC                                      SCADA, MES, クラウド
```

### 計画機能

- 仕様準拠の OPC UA サーバー
- IEC 変数の自動公開
- 設定可能な情報モデル
- 暗号化と認証
- 自動サービスディスカバリ
- 組み込みデータ履歴

---

## セキュリティ

- すべての接続に TLS 暗号化
- 証明書またはパスワードによる認証
- 変数単位のきめ細かいアクセス制御
- OPC UA セキュリティプロファイルへの準拠

---

<div style="text-align:center; padding: 2rem;">

**Bellows は開発中です。プロジェクトの進捗に応じて情報が更新されます。**

blacksmith@forgeiec.io

</div>
