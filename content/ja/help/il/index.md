---
title: "Instruction List エディタ"
summary: "IL エディタ: CR レジスタを持つ IEC 61131-3 アキュムレータベース言語"
---

## 概要

**Instruction List (IL)** は IEC 61131-3 のアセンブラライクなテキスト
言語であり、歴史的には 5 つの IEC 言語の最初のものです。プログラムは
単一の内部 **アキュムレータレジスタ** — *Current Result* (`CR`) — を
操作する命令の列です。各行は次の形式の文です:

```
[Label:] Operator [Modifier] [Operand] (* Comment *)
```

そして、アキュムレータまたは外部変数のいずれかから読み取り、または
書き込みを行います。

ForgeIEC では IL は `FIlEditor` で編集します — レイアウトとツールは
[ST エディタ](../st/) と類似しています。

## エディタのレイアウト

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (tree-sitter-instruction-list grammar) |
+----------------------------------------+
```

| 領域 | 内容 |
|---|---|
| **変数テーブル** (上) | Name、Type、Initial value、Address、Comment による宣言 — `VAR ... END_VAR` ブロックと同期。 |
| **コード領域** (下) | tree-sitter ハイライトを伴う IL ソース (`tree-sitter-instruction-list` 文法)。 |
| **検索バー** (Ctrl-F / Ctrl-H) | 検索/置換バー。 |

オンラインモードとインライン値オーバーレイは ST エディタと同様に動作
します。

## アキュムレータモデル

アキュムレータ (`CR`) は、実行中の評価の中間結果を保持します。典型的
なシーケンス:

  1. `LD x` — `x` をアキュムレータにロード (`CR := x`)
  2. `AND y` — アキュムレータと `y` を結合 (`CR := CR AND y`)
  3. `ST z` — アキュムレータを `z` に格納 (`z := CR`)

これにより IL は **スタックフリーの単一レジスタマシン** となります —
これは言語が 1993 年に標準化された当時に主流だったマイクロコントローラ
プラットフォームに非常に近いものです。

## 主要な演算子

| グループ | 演算子 | 効果 |
|---|---|---|
| **Load / Store** | `LD`, `LDN`, `ST`, `STN` | アキュムレータの設定 / アキュムレータの格納 (`N` = 否定) |
| **Set / Reset** | `S`, `R` | ビットの set / reset (BOOL 変数、`CR` = TRUE のとき) |
| **ビット論理** | `AND`, `OR`, `XOR`, `NOT` | アキュムレータをオペランドと結合 |
| **算術** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` | アキュムレータ + オペランド → アキュムレータ |
| **比較** | `GT`, `GE`, `EQ`, `NE`, `LE`, `LT` | 比較結果を `CR` に格納 |
| **ジャンプ** | `JMP`, `JMPC`, `JMPCN` | ラベルへジャンプ (`C` = `CR` = TRUE のとき) |
| **呼び出し** | `CAL`, `CALC`, `CALCN` | ファンクションブロックインスタンスを呼び出し |
| **リターン** | `RET`, `RETC`, `RETCN` | POU を抜ける |

## 修飾子

演算子はサフィックス修飾子により細分化できます:

| 修飾子 | 意味 |
|---|---|
| `N` | オペランドの **否定** (`LDN x` は `NOT x` をロード) |
| `C` | **条件付き** — `CR` = TRUE の場合にのみ実行 (`JMPC label`) |
| `(`...`)` | **括弧修飾子** — `)` が閉じるまで評価を遅延 |

括弧形式により、中間変数なしで複合式を可能にします:

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## ST ではなく IL を使うとき

今日では ST がデフォルトの選択肢です。IL は依然として以下の場合に意味
があります:

  - **マイクロコントローラのパフォーマンス** が決定的なとき — IL は
    多くの matiec バックエンドで中間最適化なしで機械命令に 1:1 で
    マッピングされます。
  - **レガシーシステム** との互換性を維持する必要があるとき (S5/S7
    AWL 由来のロジック、古い ABB / Beckhoff の既存設備)。
  - **非常にコンパクトなロジックブロック** — インターロック、ラッチ、
    エッジ条件は ST よりも IL の方が 2 行短くなることがしばしばあります。

それ以外のすべてについては、ST の方が読みやすく、保守も容易です。

## コード例 — NO/NC 接点を持つラッチコンタクタ

IL での古典的な **コンタクタ自己保持**: `start` を押すとコンタクタ `K1`
が励磁され、`stop` ボタン (NC、ローアクティブ) で再び解放されます。
ロジック:

```
K1 := (start OR K1) AND NOT stop
```

IL では:

```
PROGRAM Selbsthaltung
VAR
    start  AT %IX0.0 : BOOL;       (* NO push-button *)
    stop   AT %IX0.1 : BOOL;       (* NC push-button, low-active *)
    K1     AT %QX0.0 : BOOL;       (* contactor *)
END_VAR

    LD    start
    OR    K1                    (* CR := start OR K1 *)
    ANDN  stop                  (* CR := CR AND NOT stop *)
    ST    K1                    (* K1 := CR *)
END_PROGRAM
```

4 つの命令、1 つのレジスタ、一時的な保存なし。これは IL がもともと
設計された対象の構造そのものです。

## 関連項目

- [Structured Text](../st/) — Pascal ライクな姉妹言語
- [ライブラリ](../library/) — `CAL` で呼び出せるファンクションブロック
- [プロジェクトファイル形式](../file-format/) — `<body><IL>...` 内の IL
  本体
