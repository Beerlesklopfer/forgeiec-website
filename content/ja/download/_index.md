---
title: "ダウンロード"
summary: "ForgeIEC の全コンポーネント — APT / RPM リポジトリ、直接ダウンロード、ソースコード"
---

## ForgeIEC コンポーネント一覧

ForgeIEC は複数のコンポーネントで構成されています。必要なコンポーネントは
役割によって異なります。

| 役割 | コンポーネント | インストール先 |
|---|---|---|
| **PLC プログラマー / ユーザー** | `forgeiec-studio` | ワークステーション |
| **立ち上げエンジニア** | `forgeiec-anvil-server`（`anvild` を含む） | ターゲット PLC |
| **HMI / OPC-UA ブリッジ** | `forgeiec-bellows-server`（`bellowsd` を含む） | ターゲット PLC または別ホスト |
| **Modbus TCP** | `forgeiec-anvil-server` に含まれる | ターゲット PLC |
| **Profibus / EtherCAT / EthernetIP** | 同じく `forgeiec-anvil-server` に含まれる | ターゲット PLC |
| **操作パネル** | `forgeiec-screen-wayland` または `-xorg` | パネルのハードウェア |

---

## パッケージリポジトリからのインストール

ForgeIEC は、署名付き Debian リポジトリ（`apt.forgeiec.io`）と
署名付き RPM リポジトリ（`rpm.forgeiec.io`）で提供されています。
設定はワークステーションまたはターゲット PLC ごとに一度だけ必要です。
お使いのディストリビューションを選択してください。

{{< distro-install >}}

その後、コンポーネントを個別にインストールします。

```bash
# ワークステーション
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # デバイス記述（推奨）

# ターゲット PLC
sudo apt install forgeiec-anvil-server    # PLC ランタイム（anvild + すべての tongs-*）
sudo apt install forgeiec-bellows-server  # HMI ゲートウェイ（bellowsd）

# 操作パネル
sudo apt install forgeiec-screen-wayland  # Wayland 上のキオスク
sudo apt install forgeiec-screen-xorg     # X11 上のキオスク
```

RPM システムではコマンドが `sudo dnf install …` になり、パッケージ名は
同じです。

バスブリッジ（`tongs-modbustcp`、`tongs-ethercat`、`tongs-profibus`、
`tongs-ethernetip`）は個別のパッケージでは**ありません**。
`forgeiec-anvil-server` に含まれ、`anvild` によって起動されます。

アップデートは通常の `apt update && apt upgrade` で行います。
`.deb` ファイルを手作業で扱う必要はありません。

---

## 対応プラットフォーム

### Debian / Ubuntu（`apt.forgeiec.io`）

| パッケージ | アーキテクチャ | スイート |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | アーキテクチャ非依存 | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

スイートの対応：`bullseye` = Debian 11、`bookworm` = Debian 12、
`trixie` = Debian 13、`jammy` = Ubuntu 22.04、`noble` = Ubuntu 24.04。

### Enterprise Linux / Fedora（`rpm.forgeiec.io`）

| パッケージ | アーキテクチャ | ディストリビューション |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9（`el9`）、Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9（`el9`）、Fedora 44 |

RPM での配布は始まったばかりで、現在は操作パネルのみが対象です。
ForgeIEC Studio とランタイムは、それぞれの RPM パッケージが安定し次第
提供されます。

署名鍵は**2種類**あります。apt 用の `forgeiec.gpg`（ed25519）と
rpm 用の `forgeiec-rpm.asc`（RSA-4096）です。この違いは見た目だけの
ものではありません。RHEL 9 に含まれる `rpm` 4.16 の内蔵 PGP パーサーは
ed25519 を検証できないためです。

RPM 側では arm64 を意図的に提供していません。CI のクロスコンパイル
経路が、Enterprise Linux には存在しない Debian パッケージに依存して
いるためです。

ForgeIEC Studio の **Windows 版**：準備中です。それまでの間、Studio は
Linux 上でネイティブに、または Windows ワークステーション上で WSL2 を
介して動作します。

---

## 直接ダウンロード（リリース tarball）

パッケージリポジトリを利用できない、または利用したくない場合
（例：エアギャップ環境のワークステーション）は、Forgejo から個別の
リリースを入手できます。**リポジトリは一般公開されていません**。
SSH 公開鍵を blacksmith@forgeiec.io までお送りいただければ、
アクセスを有効にします。その後、次のリポジトリを利用できます。

- **ForgeIEC Studio のソース**：`ForgeIEC/forgeiec-studio`
- **anvild + ブリッジ**：`ForgeIEC/anvil`
- **bellowsd**：`ForgeIEC/bellows`
- **Web サイトのソース**：`ForgeIEC/forgeiec-website`

各リリースでは、署名付き `.deb` パッケージとソース tarball が
Forgejo のリリースタグに添付されます。

---

## ソースからのビルド

```bash
# リポジトリを（サブモジュールごと）クローン — SSH のみ。
# SSH 公開鍵が有効化された後に実行
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# Studio + すべてのデーモンをビルド
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# ローカルシステムに配置
./deploy.sh all
```

前提条件：

- Debian 12/13 または Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+（rustup 経由）

---

## デモプロジェクト

ForgeIEC Studio に同梱されているサンプルプロジェクト：

| プロジェクト | 目的 |
|---|---|
| `knight_rider.forge` | Bellows LED 向けの定番の流れる光テスト |
| 今後追加予定 | … |

Studio の `File → Open Example` から開けます。

---

## 次のステップ

- [ForgeIEC Studio を始める](/help/)
- [AI アシスタントの設定](/en/help/ai/)（英語）
- [バス構成](/help/bus-config/)
- [ニュース + リリースノート](/en/news/)（英語）
