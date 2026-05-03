---
title: "ヘルプ"
summary: "ForgeIECのドキュメントとリソース"
---

## ヘルプとリソース

ForgeIECヘルプセクションへようこそ。ここではプロジェクトの基盤と
理念に関する情報をご覧いただけます。

---

## トピック

### [オンラインヘルプ](/help/online/)

エディタのコンテキスト依存ヘルプの入り口。エディタで F1 を押すと、
このサイトの該当ページが開きます。URL スキームとトピックスラッグは
そちらで説明されています。

### [バス設定](/help/bus-config/)

`.forge` プロジェクトにおける産業用フィールドバス設定のための
PLCopen XML スキーマ。セグメント、デバイス、変数バインディング、
IEC アドレス割り当て。

### [テストカバレッジ](/help/tests/)

117 の自動テストが IEC 61131-3 の完全な言語機能、
132 の標準ライブラリブロック、マルチタスクスレッドシステムを検証します。

### [オープンソース哲学](/help/open-source/)

オープンソースの背後にある考え方はソフトウェアをはるかに超えています——
知識を解放し、イノベーションを民主化する運動です。

---

## はじめに

ForgeIECは2つのコンポーネントで構成されています：

1. **ForgeIECエディタ** (`forgeiec`) — ワークステーション上の開発環境
2. **ForgeIECデーモン** (`anvild`) — ターゲットPLC上のランタイムシステム

### ForgeIEC APTリポジトリからのインストール

ForgeIECは`apt.forgeiec.io`で署名済みDebianリポジトリとして
提供されています。各ワークステーションまたはターゲットPLCでの
セットアップは一度だけ必要です：

```bash
# 署名鍵をインポート
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# リポジトリソースを追加
# （Debian 12 "bookworm" または Debian 13 "trixie" — システムに合わせて）
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

標準パッケージマネージャでForgeIECパッケージをインストールできます：

```bash
# エディタ（ワークステーション）
sudo apt install forgeiec

# デーモン（ターゲットPLC）
sudo apt install anvild
```

更新は通常の`apt update && apt upgrade`ライフサイクルに従います——
手動の`.deb`ファイルは不要です。

### 対応プラットフォーム

| コンポーネント | アーキテクチャ | Debianコードネーム |
|----------------|----------------|---------------------|
| エディタ       | amd64, arm64   | bookworm, trixie    |
| デーモン       | amd64, arm64   | bookworm, trixie    |
| Bridges        | amd64, arm64   | bookworm, trixie    |
| Hearth         | amd64, arm64   | bookworm, trixie    |

### お問い合わせ

ご質問は：blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**ドキュメントはプロジェクトとともに成長します。**

blacksmith@forgeiec.io

</div>
