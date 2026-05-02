---
title: "変数の追加"
summary: "FAddVariableDialog — 1 つのモーダルですべてのフィールド、一括作成のための範囲パターン、配列ラッパー"
---

## 概要

**FAddVariableDialog** は、新しい変数を POU またはプールに追加するため
のモーダルウィンドウです。すべてのフィールドを 1 ステップで収集し、
フォームのすぐ下に結果として得られる IEC ST 宣言の **ライブプレビュー**
を表示します。入力した内容が即座に完成した `VAR ... END_VAR` スニペット
としてレンダリングされます。

このダイアログは 2 つのモードで動作します:

  - **追加モード**: フィールドが空、OK で新しい変数を作成します。
    Variables パネルのプラスアイコン、または POU エディタの Ctrl+N
    から起動します。
  - **編集モード**: パネル内の既存の変数をダブルクリック — 同じダイア
    ログで、すべてのフィールドが事前入力されています。

## フィールド

| フィールド | 必須 | 意味 |
|---|---|---|
| **Name** | はい | プログラマに見える名前。IEC 識別子規則 (英字 + 英字/数字/`_`) に対して検証されます。範囲パターンによる一括作成に使用 (下記参照)。 |
| **Type** | はい | IEC 基本型、標準 FB、プロジェクト FB、ユーザーデータ型を含むコンボ。配列の作成はラッパーチェックボックスで処理します。 |
| **Direction** | POU 依存 | 変数クラス — 下記参照。 |
| **Initial** | いいえ | 初期値 (`FALSE`, `0`, `T#100ms`, `'OFF'`)。 |
| **Address** | いいえ | VarList POU でのみ。空 = 作成時に `pool->nextFreeAddress` が自動割り当て。 |
| **Retain** | いいえ | チェックボックス — RETAIN、値が電源サイクルを生き残ります。 |
| **Constant** | いいえ | チェックボックス — `VAR CONSTANT`、実行時に書き込み不可。 |
| **Array wrapper** | いいえ | 選択された型を `ARRAY [..] OF` で包みます。 |
| **Documentation** | いいえ | 自由記述コメント。PLCopen XML に `<documentation>` として保存されます。 |

## 一括作成のための範囲パターン

`LED_0`, `LED_1`, ... `LED_7` を個別に入力する代わりに、Name フィールド
に **範囲パターン** を指定できます:

| 入力 | 効果 |
|---|---|
| `LED_0..7` | `LED_0` から `LED_7` までの 8 つの変数を作成。 |
| `LED_0-7` | 同義、同じ効果。 |
| `Sensor_1..3` | `Sensor_1` から `Sensor_3` までの 3 つの変数を作成。 |

一括作成のたびに、アドレスが設定されている場合はインクリメントされます:
`%QX0.0` → `%QX0.0`, `%QX0.1`, ..., `%QX0.7`。

## 配列ラッパーチェックボックス

**1 つ** の変数を配列として宣言したい場合は、配列チェックボックスを
オンにします。インデックス範囲用の 2 つのスピンボックスが表示され、
型は実行時に `ARRAY [..] OF <type>` でラップされます。

| Type コンボ | Array チェックボックス | インデックス範囲 | 結果として得られる宣言 |
|---|---|---|---|
| `INT` | オフ | — | `: INT;` |
| `INT` | オン | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | オン | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor` (ユーザー構造体) | オン | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

ラッパーをタイプコンボではなくチェックボックスに意図的に置いている
理由は、コンボをすっきり保ち、コンボを検索することなく任意のものの
配列を作成できるようにするためです。

## Type コンボ

このコンボは 4 つのソースを単一のリストに集約します:

  1. **IEC 基本型**: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`, `INT`,
     `DINT`, `LINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`, `TIME`,
     `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`。
  2. ライブラリの **標準 FB**: `TON`, `TOF`, `TP`, `R_TRIG`, `F_TRIG`,
     `CTU`, `CTD`, `CTUD`, `SR`, `RS`, ...
  3. **プロジェクトのファンクションブロック** — 現在のプロジェクトで
     宣言されたすべての FB (ユーザーライブラリ)。
  4. `<dataTypes>` の **ユーザーデータ型**: STRUCT、enum、エイリアス。

ARRAY テンプレートはコンボに **表示されません** — ラッパーチェックボックス
を経由します。

## POU タイプごとの Direction (変数クラス)

提供される Direction の値は POU タイプに依存します:

| POU タイプ | 利用可能な Direction |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | 固定 `VAR_GLOBAL` — コンボは非表示。 |
| `AnvilVarList` | 固定 `VAR_GLOBAL` (自動生成) — コンボは非表示。 |
| プールグローバル (POU コンテナなし) | Direction なし — `%I`/`%Q` アドレスが暗黙的に設定。 |

## 編集モード

Variables パネル内の既存の変数をダブルクリックすると、同じダイアログ
が開きます。すべてのフィールドが事前入力されており、OK で変更が
`pou->renameVariable` / `pool->rebind` 経由でルーティングされます (これ
により `byAddress` インデックスが同期し続けます)。ダイアログは
`existing != nullptr` で編集モードを検出します。

## 例 — 1 ブロックでの 8 個の LED

8 つの出力 LED をプール変数として、1 ステップで:

  - **Name**: `LED_0..7`
  - **Type**: `BOOL`
  - **Direction**: 非表示 (プールグローバル)
  - **Address**: `%QX0.0` (自動インクリメント)
  - **Initial**: `FALSE`

OK で 8 つのプールエントリが作成されます:

```text
LED_0  AT %QX0.0 : BOOL := FALSE;
LED_1  AT %QX0.1 : BOOL := FALSE;
LED_2  AT %QX0.2 : BOOL := FALSE;
LED_3  AT %QX0.3 : BOOL := FALSE;
LED_4  AT %QX0.4 : BOOL := FALSE;
LED_5  AT %QX0.5 : BOOL := FALSE;
LED_6  AT %QX0.6 : BOOL := FALSE;
LED_7  AT %QX0.7 : BOOL := FALSE;
```

その後、Variables パネルで 8 つの変数を選択し、一括操作で HMI グループ
に割り当てることができます — 例: `Set HMI Group... -> Frontpanel`。

## 関連項目

  - [変数管理](../) — カラム、フィルタ、一括操作を備えた Variables
    パネル。
  - [プロジェクトファイル形式](../../file-format/) — プールが PLCopen
    XML の `<addData>` ブロックとしてどのように永続化されるか。
