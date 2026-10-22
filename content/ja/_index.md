---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# 産業のために鍛造。

**産業品質の IEC 61131-3 開発環境。オープンソース。**

[お問い合わせ](mailto:blacksmith@forgeiec.io)

</div>

---

## 私たちが作っているもの

ForgeIECは、産業オートメーションのための完全な IEC 61131-3
開発環境です——5つのIEC言語、産業用バスシステム、リアルタイムデバッグ。

確立された商用システムと対等に渡り合うことを目指して開発されています。
すべての機能はリリース前に文書化されたテストで検証されます。

---

## なぜオープンソースか

産業オートメーションは重要な技術です。しかし、プロフェッショナルな
ツールへのアクセスは、ライセンス費用と独自仕様のシステムによって
制限されています。ForgeIECは、オートメーションの価値をすべての人に
届けます——ベンダーロックインなし、ライセンス費用なし。

オープンソースプロジェクトとして、ForgeIECはコミュニティのものです。

---

## はじめに

```bash
# 署名鍵を登録（初回のみ）
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# リポジトリを追加
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# エディタとランタイムをインストール
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

Debian 13 (trixie) の例です。Debian 12 (bookworm) または Ubuntu 24.04 (noble) では `trixie` を2か所とも置き換えてください。すべてのディストリビューション、RPM、その他のパッケージ：[ダウンロード](/download/)。

---

<div style="text-align:center; padding: 2rem;">

**産業グレードのリリースが準備でき次第、詳細情報を公開します。**

blacksmith@forgeiec.io

</div>
