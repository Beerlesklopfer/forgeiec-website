---
title: "ライブラリ (ファンクションブロック + ファンクション)"
summary: "IEC 61131-3 標準ライブラリ + ForgeIEC 拡張 + ユーザー定義ブロック"
---

## 概要

ForgeIEC ライブラリは、`.forge` プロジェクトのアプリケーションプログラム
から呼び出せる、すべての再利用可能なビルディングブロックを集約した中央
コレクションです。IEC 61131-3 標準化されたファンクションブロックおよび
ファンクションと、プロジェクト固有または ForgeIEC 固有の拡張の両方を
カバーしています。

ライブラリは **ライブラリパネル** に表示されます (デフォルトのドック位置:
右側のサイドバー)。ライブラリパネルにフォーカスがある状態で **F1** を
押すと、このページが開きます。

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (project-specific blocks)
```

ライブラリには現時点で **約 100 個のブロック** と **30 個強のファンク
ション** が同梱されています。各エントリは以下を保持します。

  - **名前** (例: `TON`, `JK_FF`)
  - **ピンリスト** (型 + 位置を含む入力 + 出力)
  - **タイプ** (状態を持つ `FUNCTION_BLOCK`、または状態を持たない
    `FUNCTION`)
  - **説明** + 使用上の注意を記載した **ヘルプテキスト**
  - **コード例** (ライブラリヘルプパネルで参照可能)

## カテゴリツリー

### Standard Function Blocks

| グループ | ブロック |
|---|---|
| **Bistable** | `SR`, `RS` — 優先度付きセット/リセット |
| **Edge Detection** | `R_TRIG`, `F_TRIG` — 立ち上がり/立ち下がりエッジ |
| **Counters** | `CTU`, `CTD`, `CTUD` — アップ/ダウン/双方向カウント |
| **Timers** | `TON`, `TOF`, `TP` — オンディレイ/オフディレイ/パルス |
| **Motion** | プロファイル、ランプ、軌跡 (準備中) |
| **Signal Generation** | テスト・検証信号用ジェネレータ FB |
| **Function Manipulators** | ホールド、ラッチ、ヒストリ |
| **Closed-Loop Control** | PID、ヒステリシス、2 点制御 |
| **Application** *(ForgeIEC)* | `JK_FF`, `DEBOUNCE` — 実用上で普遍的に有用と判明したアプリケーション寄りのブロック |

### Standard Functions

| グループ | 内容 |
|---|---|
| **Arithmetic** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` (任意の ANY_NUM 型) |
| **Comparison** | `EQ`, `NE`, `LT`, `LE`, `GT`, `GE` |
| **Bitwise** | `AND`, `OR`, `XOR`, `NOT` (ANY_BIT 型 — `help/st` を参照) |
| **Bit Shift** | `SHL`, `SHR`, `ROL`, `ROR` |
| **Selection** | `SEL`, `MAX`, `MIN`, `LIMIT`, `MUX` |
| **Numeric** | `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN` |
| **String** | `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND` |
| **Type Conversion** | `BOOL_TO_INT`, `REAL_TO_DINT`, `STRING_TO_INT`, ... |

### User Library

プロジェクトで定義されたファンクションブロックおよびファンクションです。
`FUNCTION_BLOCK` または `FUNCTION` として宣言されたものはすべて自動的
にこのカテゴリに収まり、標準ブロックと同様にプロジェクト内のあらゆる
場所から呼び出すことができます。

## ライブラリパネル — 使い方

| 操作 | 効果 |
|---|---|
| **検索** (上部のレンズアイコン) | ブロック名でツリービューをフィルタリングします — `to` と入力すると `TON` が見つかります。 |
| **ダブルクリック** (ブロック上で) | 詳細ペインでブロックのヘルプを開きます: ピンの説明 + コード例。 |
| **ドラッグ** (ST エディタへ) | カーソル位置にブロック呼び出しを挿入し、ローカル `VAR_INST` セクションへインスタンス宣言も追加します。 |
| **右クリック > "Insert Call..."** | コンテキストメニュー経由で同じ動作を実行します。 |
| **F1** (ブロック上で) | このページを開きます。 |

## 例 1 — `DEBOUNCE` によるボタンのデバウンス

`DEBOUNCE` は、機械的なボタン接点から短いノイズパルスを除去します。
`Q` は `IN` が `T_Debounce` の全期間にわたって安定して初めて変化します。
これは立ち上がりエッジ・立ち下がりエッジの両方で同じです。

### ピン配置

| ピン | 方向 | 型 | 意味 |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | 生の入力 (通常 `%IX`、機械的バウンスあり) |
| `tDebounce`  | INPUT  | `TIME` | 最小安定時間 (通常 `T#10ms`...`T#50ms`) |
| `Q`          | OUTPUT | `BOOL` | デバウンス後の出力 |

### コード例

`%IX0.0` のプッシュボタンをデバウンスし、デバウンス後の信号を単発エッジ
として自己保持コンタクタに渡す PROGRAM 本体です:

```text
PROGRAM PLC_PRG
VAR
    button_raw      AT %IX0.0 : BOOL;       (* bouncing contact *)
    button_clean    : BOOL;                  (* after DEBOUNCE *)
    button_pressed  : BOOL;                  (* single-shot per press *)
    relay_lamp      AT %QX0.0 : BOOL;        (* lamp as self-hold *)
    fbDeb           : DEBOUNCE;              (* instance *)
    fbTrig          : R_TRIG;                (* edge detector *)
END_VAR

fbDeb(IN := button_raw, tDebounce := T#20ms);
button_clean := fbDeb.Q;

fbTrig(CLK := button_clean);
button_pressed := fbTrig.Q;

(* Self-hold: toggle on every rising edge *)
IF button_pressed THEN
    relay_lamp := NOT relay_lamp;
END_IF;
END_PROGRAM
```

`DEBOUNCE` は内部的に 2 つの `TON` ブロック (上昇方向と下降方向) で
構成されています。一方は `IN` がアクティブな状態が `T_Debounce` 続いて
初めて `Q` を TRUE にし、もう一方は `IN` が非アクティブな状態が
`T_Debounce` 続いて初めて `Q` を FALSE にします。これによりフィルタは
対称になり、押下時・解放時のいずれの接点バウンスでもグリッチが発生
しません。

> **典型的な用途:** 機械式プッシュボタン、リミットスイッチ、接点ベース
> のセンサ。「1 押下につき 1 ショット」を実現するには、上記のように
> `Q` の後ろに `R_TRIG` を連結します。

## 例 2 — モードオーバーライド付き自己保持 (`JK_FF`)

`JK_FF` はボタンデバウンスを内蔵したトグルフリップフロップです。
`xButton` の安定した立ち上がりエッジごとに `Q` を TRUE と FALSE の間で
反転させます。これにより、アプリケーションプログラムが DEBOUNCE +
R_TRIG + トグルロジックを手で配線することなく、単純なプッシュボタンを
「オン/オフ」スイッチに変えることができます。

### ピン配置

| ピン | 方向 | 型 | 意味 |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | 生のボタン接点 (バウンスあり) |
| `tDebounce`  | INPUT  | `TIME` | デバウンス時間 (通常 `T#20ms`) |
| `J`          | INPUT  | `BOOL` | 「セット」(アクティブな間 `Q` を TRUE に強制) |
| `K`          | INPUT  | `BOOL` | 「リセット」(アクティブな間 `Q` を FALSE に強制) |
| `Q`          | OUTPUT | `BOOL` | 現在の状態 |
| `Q_N`        | OUTPUT | `BOOL` | 反転状態 (`NOT Q`) |
| `xStable`    | OUTPUT | `BOOL` | `xButton` が `tDebounce` の間安定している場合 TRUE |

### コード例

3 つのボタンによるランプ制御: `T1` でランプをトグル、`T_Mains` で強制
点灯 (例: 「全エリアの主照明オン」)、`T_Off` ですべて強制消灯します:

```text
PROGRAM PLC_PRG
VAR
    bButtons     AT %IX0.0 : ARRAY [0..3] OF BOOL;
    relay_lamp   AT %QX0.0 : BOOL;
    fbToggle     : JK_FF;
END_VAR

fbToggle(
    xButton    := bButtons[0],   (* toggle button T1 *)
    tDebounce  := T#20ms,
    J          := bButtons[1],   (* main light ON while held *)
    K          := bButtons[2]    (* main light OFF while held *)
);

relay_lamp := fbToggle.Q;
END_PROGRAM
```

`J`/`K` 入力の真理値表:

| `J` | `K` | 動作 |
|---|---|---|
| FALSE | FALSE | デバウンス済みの押下ごとにトグル |
| TRUE  | FALSE | Q := TRUE (セット、トグルを上書き) |
| FALSE | TRUE  | Q := FALSE (リセット、トグルを上書き) |
| TRUE  | TRUE  | 未定義 — 避けること |

`xStable` を使うと「ボタンが現在押されている」ロジックを実装できます
(例: トグルの効果が現れるのを待たずに押下を可視化する LED など)。

## エディタと PLC 間のライブラリ同期

標準ライブラリは 2 か所に存在します:

  - **エディタ側:** `editor/resources/library/standard_library.json`
    (Qt のリソースシステムを介して `.exe` にコンパイル組込み)。
  - **PLC 側:** anvild サブモジュール内の同一 JSON ファイル。アップロード
    された C ソースに対する `make` ステップで取り込まれます。

**ライブラリ同期** は接続時に両バージョンの SHA-256 を比較します。差分
が検出されると Output パネルにヒントが表示され、その後の動作は設定可能
です:

  - `Preferences > Library > Auto-Push` オフ (デフォルト): `Tools > Sync
    Library` から手動でプッシュします。古いエディタからの偶発的な上書き
    に対して、本番ランタイムを保護します。
  - `Preferences > Library > Auto-Push` オン: 差分検出で自動的にプッシュ
    します。プログラマが 1 名の開発環境で便利です。

## ForgeIEC 拡張

以下のブロックは IEC 61131-3 では標準化されていませんが、実用上で普遍
的に有用と判明したため、標準ライブラリの一部として同梱されています:

| ブロック | 目的 |
|---|---|
| `JK_FF` | ボタンデバウンス内蔵のトグルフリップフロップ (例 2 を参照)。 |
| `DEBOUNCE` | 対称的なボタンデバウンス (例 1 を参照)。 |

これらのブロックは *Standard Function Blocks / Application* に配置され、
JSON ソース内で `isStandard: true` フラグが付いて「削除不可」(つまり
ライブラリパネルから誤って削除されないよう) マークされています。

## ユーザーライブラリへの独自ブロックの追加

現在のプロジェクト内のすべての `FUNCTION_BLOCK` および `FUNCTION` 宣言
は、自動的に **User Library** に登録されます。可視化のタイミング:

  1. **ライブラリパネル:** POU を宣言・保存した直後。
  2. **コード補完 (Ctrl-Space):** 即時。
  3. **FBD/LD エディタのブロックとして:** 即時。
  4. **PLC 上では** `Compile + Upload` 後。

複数プロジェクトで再利用するには `File > Export POU...` から POU を
`.forge-pou` ファイルとしてエクスポートし、対象プロジェクトでインポート
してください。プロジェクト横断の「ワークスペースライブラリ」はバック
ログに登録されています。

## 関連項目

- [Structured Text 構文](../st/) — ST でのブロック呼び出しの記法。
- [Function Block Diagram エディタ](../fbd/) — ブロックをグラフィカルに
  配線する方法。
- [Variables パネル](../variables/) — アドレスプールがインスタンスを
  どう認識するか。
