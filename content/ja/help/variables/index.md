---
title: "変数管理"
summary: "FAddressPool への中央ビューとしての Variables パネル — カラム、フィルタ、一括操作、安全スイッチ"
---

## 概要

**Variables パネル** は **FAddressPool** への中央ビューです。
FAddressPool は ForgeIEC プロジェクト内のすべての変数の単一の真実の
ソースです。各変数はプール内に正確に 1 回だけ存在し、IEC アドレス
(`%IX0.0`, `%QW3`, ...) をキーとします。GVL、AnvilVarList、HmiVarList、
POU インタフェースなどのコンテナはこのプールの **ビュー** に過ぎず、
変数が 2 つのストアに並行して存在することはありません。

```
FAddressPool  (single source of truth)
   |
   +-- FAddressPoolModel  (Qt table)
         |
         +-- FVariablesPanel  (filters + bulk ops + clipboard)
               |
               +-- Tree filter sets FilterMode + tag
```

このパネルはメインウィンドウの下部にドックされ、すべての変更を直ちに
他のすべてのビュー (POU エディタ、ST コンパイラ、PLCopen-XML 保存) に
反映します。

## カラム

テーブルには **15 個のカラム** があります。各カラムはヘッダのコンテキスト
メニューから個別に表示/非表示できます。各 POU エディタのインスタンス
は、カラム可視性を独立して保存します。

| カラム | 内容 |
|---|---|
| **Name** | プログラマに見える名前。修飾されたプール項目はフルパスで表示されます: `Anvil.Pfirsich.T_1`, `Bellows.Stachelbeere.T_Off`, `GVL.Motor.K1_Mains`。 |
| **Type** | IEC 基本型またはユーザー定義型。配列は `ARRAY [0..7] OF BOOL` のように表示されます。 |
| **Direction** | IEC 変数クラス: POU ローカルでは `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP`、プールグローバルでは `in`/`out` (`%I` か `%Q` から導出)。 |
| **Address** | IEC アドレス — 主キー。ビット入力には `%IX0.0`、ワード出力には `%QW1`、マーカービットには `%MX10.3`。 |
| **Initial** | 初期値 (`FALSE`, `0`, `T#100ms`, `'OFF'`)。最初のサイクルで変数にロードされます。 |
| **Bus Device** | この変数がバインドされているバスデバイス (Modbus スレーブなど) の UUID — コンボボックスとして編集可能。 |
| **Bus Addr** | スレーブに対する Modbus レジスタオフセット (`0`, `1`, ...)。 |
| **R** (Retain) | チェックボックス — 値が電源サイクルを生き残るか? |
| **C** (Constant) | チェックボックス — IEC 定数 (`VAR CONSTANT`)、実行時に書き込み不可。 |
| **RO** (ReadOnly) | チェックボックス — プログラムコードから読み取り専用。 |
| **Sync** | マルチタスク同期クラス (`L`/`A`/`D`)。直近の ST コンパイラ実行で生成されます。 |
| **Used by** | この変数を読み書きするタスク。例: `PROG_Fast (R/W), PROG_Slow (R)`。 |
| **Monitor** / **HMI** / **Force** | 変数ごとの安全スイッチ。バックログの **クラスタ A** — 明示的なオプトインで、`hmiGroup` タグとは区別されます。ST コンパイラはコード生成前に、Force/HMI アクセスがフラグを持つ変数のみを対象としていることを検証します。 |
| **Live** | オンラインモードでの実行時値 (anvild ライブ値ストアから供給。切断時は非表示)。 |
| **Scope** | オシロスコープ可視性チェックボックス — 変数をスコープパネルに送信します。 |
| **Documentation** | 自由記述コメント。 |

## フィルタモード

このパネルはプール全体を一度に表示しません — **左側のプロジェクト
ツリー** が表示するスライスを選択します。ツリーノードをクリックすると、
メインウィンドウは `FilterMode` とタグを設定します:

| FilterMode | 表示内容 |
|---|---|
| `FilterAll` | プール全体 — タグ制限なし。 |
| `FilterByGvl` | `gvlNamespace == tag` の変数 (例: `GVL.Motor` のみ)。 |
| `FilterByAnvil` | `anvilGroup == tag` の変数 (1 つの Anvil IPC グループ)。 |
| `FilterByHmi` | `hmiGroup == tag` の変数 (1 つの Bellows HMI グループ)。 |
| `FilterByBus` | `busBinding.deviceId == tag` の変数 (1 つのバスデバイスのすべての変数)。 |
| `FilterByModule` | `FilterByBus` と同様、加えて `moduleSlot` — タグ形式 `hostname:slot`。 |
| `FilterByPou` | POU ローカル — `pouInterface == tag` の変数。 |
| `FilterCommentsOnly` | コメント区切りのみ、変数なし。 |

## フィルタ軸 (組み合わせ可能)

テーブルの上には、ツリーフィルタの上に並列に作用する 4 つの追加軸が
あります:

  - **フリーテキスト検索** (名前、アドレス、タグ全体に対して) — `to` で
    `T_Off` が見つかります。
  - **IEC 型フィルタ** (コンボとして: `all` / `BOOL` / `INT` / `REAL` / ...)。
  - **アドレス範囲フィルタ**: `all` / `%I` (入力) / `%Q` (出力) / `%M`
    (マーカー)。`%M` 内ではさらにワードサイズで分類 (`%MX` / `%MW` /
    `%MD` / `%ML`)。
  - **TaggedOnly トグル** — コンテナタグを持たないプールエントリをすべて
    非表示 (「孤立した」プールを見つけるのに有用)。

各フィルタは AND で結合されます: アクティブなすべての軸に一致しない
ものは非表示になります。

## マルチセレクト + 一括操作

任意の Qt テーブルと同様: Shift クリックと Ctrl クリックで範囲または
個別行を選択します。選択に対するコンテキストメニューでは以下を提供
します:

  - **Set Anvil Group...** — 選択されたすべての変数に `anvilGroup` を
    設定。
  - **Set HMI Group...** — `hmiGroup` についても同様。
  - **Set GVL Namespace...** — `gvlNamespace` についても同様。
  - **Clear Tag** — アクティブなフィルタモードのタグを削除。
  - **Toggle Monitor / HMI / Force** — 安全スイッチの一括トグル。

すべての一括編集は `FAddressPoolModel::applyToRows` を経由し、単一の
`dataChanged` シグナルを発生させ、1 つのアンドゥステップとしてアンドゥ
可能です。

## クリップボード (コピー / カット / ペースト)

選択された変数は **すべてのタグとフラグとともに** コピーでき、別の
ビューにペーストできます。ペイロードは 2 つの形式を使用します:

  - **カスタム MIME** (`application/x-forgeiec-vars+json`) — 完全なプール
    情報を保持するラウンドトリップ手段。
  - **TSV プレーンテキスト** — Excel / テキストエディタ用のフォール
    バック。

**ペースト時** にパネルはコンテナタグを **アクティブなフィルタモード**
に自動的に再ターゲットします: `FilterByAnvil` (グループ `Pfirsich`) から
コピーして `FilterByHmi` (グループ `Stachelbeere`) にペーストすると、
変数は `anvilGroup` を捨てて `hmiGroup = Stachelbeere` を取得します。
重複したアドレスと名前は重複排除されます (`T_1` → `T_1_1`)。

## HmiVarList へのドラッグ&ドロップ

メインパネルから変数を HmiVarList POU にドラッグできます。エディタは
自動的に変数の **HMI エクスポートフラグ** を設定し、HMI グループをタグ
として書き込みます — Bellows のエクスポート準備が整った状態になります。

## 変数ごとの安全スイッチ

3 つの変数ごとのスイッチ。それぞれ明示的なオプトインを必要とします:

  - **HMI** — Bellows が変数を読み書きすることを許可。
  - **Monitor** — オンラインモードでのライブ観測を許可。
  - **Force** — 実行時値の強制を許可。

これらのフラグは **`hmiGroup` タグとは別** です。タグはグループ所属を
記述し、フラグは効果を有効化します。各コード生成の前に ST コンパイラ
は、すべての Bellows または Force アクセスがフラグの設定された変数を
対象としているかを検証します — そうでない場合はコンパイルエラーを
発生させます。

## 関連項目

  - [変数の追加](add/) — 範囲パターンと配列ラッパーを備えた
    `FAddVariableDialog`。
  - [プロジェクトファイル形式](../file-format/) — プールが PLCopen XML
    の `<addData>` ブロックとしてどのように永続化されるか。
  - [ライブラリ](../library/) — ファンクションブロックがプール内の
    インスタンスをどう認識するか。
