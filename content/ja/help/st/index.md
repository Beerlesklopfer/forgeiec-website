---
title: "Structured Text エディタ"
summary: "ST エディタ + 言語の基礎: IEC 61131-3 の文、ビットアクセス、修飾プール参照"
---

## 概要

**Structured Text (ST)** は IEC 61131-3 の Pascal ライクな高水準言語
であり、ForgeIEC における PROGRAM、FUNCTION_BLOCK、FUNCTION POU の
デフォルトエディタです。エディタは `QWidget` ベースの構成で、変数
テーブルとコード領域を垂直スプリッタで結合しています。

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT/VAR_INST)    |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (Tree-sitter highlighting + folding +  |
|  Ctrl-Space completion)                |
+----------------------------------------+
```

## エディタのレイアウト

| 領域 | 内容 |
|---|---|
| **変数テーブル** (上) | Name、Type、Initial value、Address、Comment のカラムによる宣言。編集はコードの `VAR ... END_VAR` ブロックにライブで同期されます。 |
| **コード領域** (下) | 変数セクション間の ST ソース。tree-sitter AST が駆動する行折りたたみ、行番号、カーソル行のハイライト。 |
| **検索バー** (Ctrl-F / Ctrl-H) | コード領域の上に表示され、検索/置換用の置換モードを備えます。 |

スプリッタはレイアウト状態の中で POU ごとに位置を記憶します。

## Tree-sitter による構文ハイライト

正規表現ベースの `QSyntaxHighlighter` の代わりに、ForgeIEC は ST ソース
を **Tree-sitter** で AST にパースし、キャプチャクエリでカラーリング
します:

  - **キーワード** (`IF`, `THEN`, `FOR`, `FUNCTION_BLOCK`, ...): マゼンタ
  - **データ型** (`BOOL`, `INT`, `REAL`, `TIME`, ...): シアン
  - **文字列 + 時間リテラル** (`'abc'`, `T#20ms`): 緑
  - **コメント** (`(* ... *)`, `// ...`): 灰色、イタリック
  - **PUBLISH / SUBSCRIBE**: Anvil 拡張キーワード、専用スタイル

利点: 複雑な構造 (ネストされたコメント、時間リテラル、修飾参照) でも
ハイライトが正しく保たれ、同じ AST がコード折りたたみの折りたたみ可能
範囲も駆動します。

## コード補完 (Ctrl-Space)

**Ctrl-Space** を押すか、2 つの一致する文字を入力すると、補完ポップ
アップが開きます。コンプリータは以下を認識します:

  - **IEC キーワード** (`IF`, `CASE`, `FOR`, `WHILE`, `RETURN`, ...)
  - **データ型** (`BOOL`, `INT`, `DINT`, `REAL`, `STRING`, `TIME`, ...)
  - 現在の POU の **ローカル変数**
  - プロジェクトの **POU 名** (PROGRAM, FUNCTION_BLOCK, FUNCTION)
  - **ライブラリブロック** (`TON`, `R_TRIG`, `JK_FF`, `DEBOUNCE`, ...)
  - **標準ファンクション** (`ABS`, `SQRT`, `LIMIT`, `LEN`, ...)

変数プールへの変更 (`poolChanged` シグナル) は 100 ms のデバウンスで
補完モデルに伝播します — 新しいプールエントリはほぼ即座に利用可能に
なり、すべてのキーストロークで完全な再スキャンが発生することはありません。

## 言語の基礎 (IEC 61131-3)

### 文

| 文 | 形式 |
|---|---|
| **代入** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | ループを抜ける / POU を抜ける |

### 式

IEC の優先順位に従う標準演算子: `**`、単項 `+/-/NOT`、`* / MOD`、`+ -`、
比較、`AND / &`、`XOR`、`OR`。括弧は Pascal と同様。暗黙の数値型変換
は許可されていません — `INT_TO_DINT`、`REAL_TO_INT` などは明示的に
呼び出す必要があります。

### ANY_BIT 型に対するビットアクセス

`var.<bit>` は `BYTE`/`WORD`/`DWORD`/`LWORD` 変数に対して、単一ビットを
直接抽出または設定します:

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

コンパイラはこれを補助変数なしで `AND`/`OR`/シフトによるクリーンな
ビットマスキングに変換します。

### 3 階層の修飾参照

`<Category>.<Group>.<Variable>` は GVL を明示的に宣言することなく、
プールエントリに直接アクセスします:

| プレフィックス | ソース |
|---|---|
| `Anvil.X.Y`   | `anvilGroup="X"` のプールエントリ |
| `Bellows.X.Y` | `hmiGroup="X"` のプールエントリ |
| `GVL.X.Y`     | `gvlNamespace="X"` のプールエントリ |
| `HMI.X.Y`     | `Bellows.X.Y` の同義語 |

`Anvil.X.Y` と `Bellows.X.Y` は独立に異なるプールエントリを指すことが
できます — IEC アドレスが異なる場合、コンパイラは即座に別の C シンボル
を出力します。

### 配置済み変数 (`AT %...`)

配置済み変数は宣言を IEC アドレスにバインドします:

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

アドレスはプール内の主キーです — [プロジェクトファイル形式](../file-format/)
を参照してください。

## コード例

### 例 1 — ライブラリブロックでの TON 呼び出し

```text
PROGRAM PLC_PRG
VAR
    start_button   AT %IX0.0  : BOOL;
    motor_run      AT %QX0.0  : BOOL;
    fbDelay        : TON;
END_VAR

fbDelay(IN := start_button, PT := T#3s);
motor_run := fbDelay.Q;
END_PROGRAM
```

`fbDelay` はライブラリ FB `TON` のインスタンスです。`start_button` が
3 秒間保持されると、`motor_run` が TRUE に切り替わります。

### 例 2 — Bellows の読み取りで出力を駆動

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` および `Anvil.Sensors.contact_door` は、コンパイラ
が GVL 宣言なしに解決する 3 階層参照です — ただし両方のタグがアドレス
プールに保持され、`Pfirsich` グループの HMI エクスポートがアクティブで
あることが条件です。

## 関連項目

- [ライブラリ](../library/) — 利用可能なファンクションブロック + ファ
  ンクション
- [Instruction List](../il/) — 代替テキストエディタ (アキュムレータ
  ベース)
- [プロジェクトファイル形式](../file-format/) — ST コードが `.forge`
  にどのように保存されるか
