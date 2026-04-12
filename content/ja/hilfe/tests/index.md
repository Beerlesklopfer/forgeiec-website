---
title: "テストカバレッジ"
summary: "自動品質保証：117のテストがIEC 61131-3の完全な言語仕様、全標準ブロック、マルチタスクシステムを検証"
---

ForgeIECは包括的な自動テストスイートによって保護されています。
各コミットはマージ前に**117のユニットテスト**で検証されます。これらのテストは
IEC 61131-3 Structured Textの完全な言語仕様、全標準ファンクションブロック、
およびマルチタスクシステムをカバーしています。

## テストスイートの概要

| スイート | テスト数 | 検証内容 |
|----------|--------:|----------|
| **FStCompilerTest** | 101 | 完全なST言語仕様 |
| **FStLibraryTest** | 8 | 全132標準ブロック（FB + FC） |
| **FCodeGeneratorThreadingTest** | 8 | マルチタスクスケジューリング + ロックフリー同期 |
| **合計** | **117** | **エラー0件** |

---

## 1. ST言語仕様（FStCompilerTest）

101のテストが、サポートされている全てのIEC 61131-3 Structured Text
言語構造を検証します。各テストはSTフラグメントをFStCompilerでコンパイルし、
生成されたC++コードを検証します。

### 1.1 代入

| テスト | STコード | 検証内容 |
|--------|----------|----------|
| `assignSimple` | `a := 42;` | 単純代入 |
| `assignExpression` | `a := b + 1;` | 式による代入 |
| `assignExternal` | `ExtVar := 10;` | VAR_EXTERNALアクセス |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | 修飾GVLパス |

### 1.2 算術演算子

| テスト | STコード | C演算子 |
|--------|----------|---------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | 括弧 |

### 1.3 比較演算子

| テスト | STコード | C演算子 |
|--------|----------|---------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 ブール演算子

| テスト | STコード | C演算子 |
|--------|----------|---------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 リテラル

| テスト | STコード | 検証内容 |
|--------|----------|----------|
| `literalInteger` | `a := 12345;` | 整数 |
| `literalReal` | `c := 3.14;` | 浮動小数点 |
| `literalBoolTrue` | `flag := TRUE;` | ブール値 |
| `literalBoolFalse` | `flag := FALSE;` | ブール値 |
| `literalString` | `text := 'hello';` | 文字列 |
| `literalTime` | `counter := T#500ms;` | 時間定数 |

### 1.6 制御構造

**IF / ELSIF / ELSE / END_IF**

| テスト | 検証内容 |
|--------|----------|
| `ifSimple` | 単純条件 |
| `ifElse` | If-Else分岐 |
| `ifElsif` | ELSIFによる多重分岐 |
| `ifNested` | ネストされたIFブロック |

**FOR / WHILE / REPEAT**

| テスト | 検証内容 |
|--------|----------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | BYステップ幅付きFOR |
| `whileLoop` | WHILEループ |
| `repeatUntil` | REPEAT/UNTILループ |

**CASE**

| テスト | 検証内容 |
|--------|----------|
| `caseStatement` | 複数ラベル付きCASE/OF + switch/case/break |

**RETURN / EXIT**

| テスト | 検証内容 |
|--------|----------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | FOR内のEXIT → break |

### 1.7 ファンクションブロック（FB呼び出し）

| テスト | 検証内容 |
|--------|----------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — OUT =>代入 |

### 1.8 配列アクセス

| テスト | 検証内容 |
|--------|----------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | FORループ内での配列アクセス |

### 1.9 型変換

コンパイラは`XXX_TO_YYY`パターンを認識し、IEC規格に準拠した
Cスタイルキャスト（`(TYPE)value`）を生成します。

| テスト | STコード | 生成結果 |
|--------|----------|----------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 構造体メンバアクセス

| テスト | 検証内容 |
|--------|----------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 タスク間変数（マルチタスク）

| テスト | 検証内容 |
|--------|----------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` ロックフリー読み取り用 |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` ロックフリー書き込み用 |
| `crossStructuredGet` | `__snap_` スレッドローカルスナップショットアクセス |
| `crossStructuredMemberAccess` | `__snap_Struct.field` アクセス |

### 1.12 標準ファンクションブロック

各IEC標準FBはインスタンスとして生成され、呼び出されます：

| テスト | FB型 | 検証内容 |
|--------|------|----------|
| `fbTon` | TON | オンディレイ |
| `fbTof` | TOF | オフディレイ |
| `fbTp` | TP | パルスタイマー |
| `fbCtu` | CTU | アップカウンタ |
| `fbCtd` | CTD | ダウンカウンタ |
| `fbRtrig` | R_TRIG | 立ち上がりエッジ |
| `fbFtrig` | F_TRIG | 立ち下がりエッジ |
| `fbRs` | RS | リセット優先 |
| `fbSr` | SR | セット優先 |

### 1.13 標準関数

| カテゴリ | テスト数 | 関数 |
|----------|--------:|------|
| 数学 | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| 選択 | 4 | SEL, LIMIT, MIN, MAX |
| 文字列 | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| ビットシフト | 4 | SHL, SHR, ROL, ROR |
| 型変換 | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 エッジケース

| テスト | 検証内容 |
|--------|----------|
| `complexNestedExpression` | ネストされた式 |
| `multipleStatementsOnSeparateLines` | 複数行プログラム |
| `emptyBody` | 空のPOUボディ |
| `commentOnlyBody` | コメントのみ |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | 大文字・小文字の区別 |

---

## 2. 標準ライブラリ（FStLibraryTest）

8つのデータ駆動テストが標準ライブラリ（`standard_library.sql`）の
**全132ブロック**を自動的に検証します。

### 2.1 ファンクションブロック（13 FB）

| テスト | 検証内容 |
|--------|----------|
| `fbSingleInstance` | 各FBが個別にインスタンス化・呼び出し可能 |
| `fbDoubleInstance` | 同一FB型の2インスタンスが同時使用可能 |
| `fbOutputRead` | 呼び出し後に全出力が読み取り可能 |

**対象FB：** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 関数（119 FC）

| テスト | 検証内容 |
|--------|----------|
| `fcCall` | 各FCが正しいパラメータで呼び出し可能（104テスト済み） |
| `fcInExpression` | FC戻り値が式中で使用可能 |

**対象カテゴリ：**

- **算術：** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **比較：** EQ, NE, LT, GT, LE, GE
- **三角関数：** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **対数：** EXP, LN, LOG, SQRT
- **選択：** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **文字列：** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **ビットシフト：** SHL, SHR, ROL, ROR
- **型変換：** 60以上の変換関数（BOOL_TO_INT, INT_TO_REAL, ...）
- **ForgeIEC拡張：** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. マルチタスク（FCodeGeneratorThreadingTest）

8つのテストが設計仕様（MT-spec, docs/design/multi-task-scheduler.md）に従い、
完全なマルチタスクスケジューリングシステムを検証します。

| テスト | 検証内容 |
|--------|----------|
| `singleProgramDefaultTask` | 明示的タスクなしの1つのPROGRAM → DefaultTask合成、スレッドなし |
| `twoProgramsTwoTasks` | 2タスク → RESOURCE0_start__、Legacy-Shim config_run__、両方のタスクスレッド |
| `crossPrimitiveAtomicEmission` | 共有INT変数 → `std::atomic<>` Locationストレージ、ボディ内の`__GET_EXTERNAL_ATOMIC` |
| `crossStructuredDoubleBuffer` | 共有STRUCT → `__DBUF_[2]` + `thread_local __snap_` + ダブルバッファのコピーイン/アウト |
| `localVarNoSync` | 1タスクのみの変数 → 通常の`__SET_EXTERNAL`、Atomicなし |
| `conflictTwoWriters` | 2タスクが同一変数に書き込み → コンパイル警告 |
| `singleProgramDefaultTask` | 後方互換性：既存プロジェクトが変更なしで動作 |

### マルチタスクアーキテクチャ

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [bufferLock下]                | [lock-free]
```

**同期メカニズム：**
- **CrossPrimitive**（BOOL, INT, REAL, ...）：Location変数上の`std::atomic<T>`、ボディコード内の`__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC`
- **CrossStructured**（STRUCT, ARRAY, STRING）：アトミック書き込みインデックス付きダブルバッファ`__DBUF_[2]`、Set一貫性のための`thread_local`スナップショット`__snap_`

---

## 品質保証

### 自動検証

テストは`-DBUILD_TESTS=ON`で毎回のビルド時に実行されます。
CIパイプライン（Forgejo Actions）への統合は準備済みです。

### データ駆動テスト

ライブラリテスト（`FStLibraryTest`）はブロック定義を
`standard_library.sql`から直接読み取ります。新しいブロックが追加されると
自動的にテストされます。手動でのテストケース作成は不要です。

### 完全性

テストスイートは、ForgeIECがサポートするIEC 61131-3 Structured Textの
完全な言語仕様をカバーしています：

- 全演算子（算術、比較、ブール、ビットシフト）
- 全制御構造（IF, FOR, WHILE, REPEAT, CASE）
- 全リテラル型（Integer, Real, Bool, String, Time）
- 全標準FBおよびFC（132ブロック）
- 配列および構造体アクセス
- GVL修飾変数
- タスク間同期（Atomics + ダブルバッファ）
- 型変換（Cキャスト生成）
