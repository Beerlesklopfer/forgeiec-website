---
title: "環境設定"
summary: "中央のエディタ設定ダイアログ: Editor、Runtime、PLC、AI Assistant"
---

## 概要

**Preferences ダイアログ** は、すべてのエディタグローバル設定への単一
のエントリポイントです。開いているプロジェクトの一部ではなく、エディタ
自体、ランタイムへの接続、アップロード後の動作を構成するすべての項目
を扱います。

ダイアログは **`Edit > Preferences...`** から開きます (一部のテーマでは
`Tools > Preferences...` に配置されます)。ダイアログにフォーカスがある
状態で **F1** を押すと、このページが直接開きます。

```
Preferences
+-- Editor          (font, tab width, line numbers)
+-- Runtime         (anvild host/port, Anvil debug, network scanner)
+-- PLC             (build mode, auto-start, persist, monitoring)
+-- AI Assistant    (LLM endpoint, tokens, temperature)
```

## Editor

ST コードエディタおよびその他のすべてのテキスト入力フィールドにおける
テキストの表示方法を制御します。

| フィールド | 意味 |
|---|---|
| **Font**         | フォントファミリ。等幅フォントに事前フィルタ済み (推奨: `JetBrains Mono`, `Cascadia Code`, `Consolas`)。 |
| **Font size**    | フォントサイズ (ポイント)。デフォルト `10`。 |
| **Tab width**    | タブストップごとのスペース数。デフォルト `4`。 |
| **Show line numbers** | コードエディタの余白に行番号を表示します。 |

## Runtime

**anvild** デーモンへの接続および IPC 診断。

| フィールド | 意味 |
|---|---|
| **Host**         | PLC ホスト名または IP。デフォルト `localhost`。 |
| **Port**         | anvild の gRPC ポート。デフォルト `50051`。 |
| **User**         | トークン認証用のユーザー名。 |
| **Anvil Debug**  | IPC 診断レベル (`Off`, `Errors only`, `Verbose`)。anvild ログに追加の統計を加えます — 本番環境での Iceoryx トピックドリフトの追跡に有用です。 |

加えて: **Auto-Connect on start** はエディタ起動時に最後に成功裏に接続
された anvild に自動的に接続します。専用のエンジニアリングラップトップ
で便利です。

同じタブの **Network Scanner** ブロックは、Modbus TCP デバイス (ポート
502) と ForgeIEC ランタイム (ポート 50051) を求めて LAN をスキャンし、
ヒットしたものをバス設定に挿入します。

## PLC

PLC への **Upload** 後の動作を制御します。

| フィールド | 意味 |
|---|---|
| **Compile Mode** | `Development` (ライブモニタリング + Force 有効) または `Production` (ストリップ済みバイナリ、デバッグブリッジなし — セキュリティ境界)。 |
| **PLC autostart**| アップロード成功後に PLC ランタイムを自動的に開始し、確認ダイアログをスキップします。 |
| **Persist enabled** | `VAR_PERSIST`/`RETAIN` 変数の `/var/lib/anvil/persistent.dat` への定期的な永続化を有効化します。値はランタイム再起動後も維持されます。 |
| **Persist polling interval** | 自動保存パスの間隔 (秒、デフォルト `5 s`)。 |
| **Monitor history** | オシロスコープレコーダーの変数ごとのサンプル数 (デフォルト `1000`)。 |
| **Monitor interval**| ライブモニタリングのサンプル間隔 (ミリ秒、デフォルト `100 ms`)。 |

## Library

エディタリソースと PLC 側ライブラリパス間の標準ライブラリの同期動作 —
完全なドリフトモデルについては [ライブラリ](../library/) を参照して
ください。2 つのモードがあります:

  - **Auto-Push オフ** (デフォルト) — 接続時、ドリフトが検出されると
    エディタは Output パネルにヒントをログ記録するだけです。プッシュは
    `Tools > Sync Library` から手動で行います。
  - **Auto-Push オン** — 検出されたドリフトごとに、エディタはローカル
    ライブラリのバージョンを自動的にプッシュします。1 名のプログラマ
    の環境で有用です。

## AI Assistant

ローカルの OpenAI 互換 LLM サーバー (LM Studio, Ollama, llama.cpp,
vLLM) に対するオプションのコード補完。

| フィールド | 意味 |
|---|---|
| **Enable AI Assistant** | インライン補完をトグルします。 |
| **API Endpoint**        | OpenAI 互換エンドポイント (例: `http://localhost:1234/v1`)。 |
| **Max Tokens**          | リクエストごとの応答上限。デフォルト `2048`。 |
| **Temperature**         | `Precise (0.1)`, `Balanced (0.3)`, `Creative (0.7)`, `Wild (1.0)`。 |

## UX 状態 (自動永続化)

以下のフィールドは Preferences ダイアログを介さずに **バックグラウンド**
で保存され、エディタは終了したときの正確な状態で再オープンします:

  - ウィンドウのジオメトリ + ウィンドウ状態 (`windowGeometry`,
    `windowState`)
  - スプリッタおよびヘッダ位置 (`splitterState`, `headerState`)
  - Output パネルの高さ (`outputPanelHeight`)
  - 最後に開いたプロジェクト (`lastProject`) と最近使用したファイル
    リスト
  - セッション状態: 開いている POU タブ、アクティブなタブ、POU ごとの
    カーソルとスクロール位置

## 設定の保存

設定は Qt の `QSettings` を介して、プラットフォーム固有に保存されます:

| プラットフォーム | パス |
|---|---|
| **Windows** | レジストリ: `HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

該当するファイル / レジストリキーを削除すると、すべての設定がデフォルト
にリセットされます — 失敗したアップグレード後に有用です。

## 計画中の拡張

バックログ (クラスタ R フェーズ 3): Output パネルは独自の重大度色 (エラー
赤、警告黄、情報白) と設定可能なフォントサイズを取得します。これらの
オプションは、その後ここの新しい `Output` タブに表示されます。

## 関連項目

  - [ライブラリ](../library/) — エディタとランタイム間の同期動作。
  - [バス設定](../bus-config/) — ここではなく、バスセグメント / デバイス
    自体に存在するプロジェクトスコープの設定。
