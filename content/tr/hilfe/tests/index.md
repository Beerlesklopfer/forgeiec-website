---
title: "Test Kapsamı"
summary: "Otomatik kalite guvencesi: 117 test, IEC 61131-3 dil dagarcigininin tamami, tum standart bloklar ve coklu gorev sistemi dogrulanir"
---

ForgeIEC kapsamli bir otomatik test paketi ile korunmaktadir.
Her commit, merge oncesi **117 birim testi** ile dogrulanir. Bu testler
IEC 61131-3 Structured Text dil dagarcigininin tamami, tum standart
fonksiyon bloklari ve coklu gorev sistemini kapsar.

## Test Paketlerine Genel Bakis

| Paket | Test | Dogrular |
|-------|-----:|----------|
| **FStCompilerTest** | 101 | Tam ST dil dagarcigi |
| **FStLibraryTest** | 8 | Tum 132 standart blok (FB + FC) |
| **FCodeGeneratorThreadingTest** | 8 | Coklu gorev zamanlamasi + kilitsiz senkronizasyon |
| **Toplam** | **117** | **0 hata** |

---

## 1. ST Dil Dagarcigi (FStCompilerTest)

101 test, desteklenen her IEC 61131-3 Structured Text dil yapisini dogrular.
Her test, bir ST parcasini FStCompiler ile derler ve
uretilen C++ kodunu dogrular.

### 1.1 Atamalar

| Test | ST Kodu | Dogrular |
|------|---------|----------|
| `assignSimple` | `a := 42;` | Basit atama |
| `assignExpression` | `a := b + 1;` | Ifadeli atama |
| `assignExternal` | `ExtVar := 10;` | VAR_EXTERNAL erisimi |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | Nitelikli GVL yolu |

### 1.2 Aritmetik operatorler

| Test | ST Kodu | C Operatoru |
|------|---------|-------------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | Parantezleme |

### 1.3 Karsilastirma operatorleri

| Test | ST Kodu | C Operatoru |
|------|---------|-------------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 Mantiksal operatorler

| Test | ST Kodu | C Operatoru |
|------|---------|-------------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 Degerler

| Test | ST Kodu | Dogrular |
|------|---------|----------|
| `literalInteger` | `a := 12345;` | Tam sayi |
| `literalReal` | `c := 3.14;` | Kayan nokta |
| `literalBoolTrue` | `flag := TRUE;` | Mantiksal deger |
| `literalBoolFalse` | `flag := FALSE;` | Mantiksal deger |
| `literalString` | `text := 'hello';` | Karakter dizisi |
| `literalTime` | `counter := T#500ms;` | Zaman sabiti |

### 1.6 Kontrol yapilari

**IF / ELSIF / ELSE / END_IF**

| Test | Dogrular |
|------|----------|
| `ifSimple` | Basit kosul |
| `ifElse` | If-Else dallanmasi |
| `ifElsif` | ELSIF ile coklu dallanma |
| `ifNested` | Ic ice IF bloklari |

**FOR / WHILE / REPEAT**

| Test | Dogrular |
|------|----------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | BY adim genisligi ile FOR |
| `whileLoop` | WHILE dongusu |
| `repeatUntil` | REPEAT/UNTIL dongusu |

**CASE**

| Test | Dogrular |
|------|----------|
| `caseStatement` | CASE/OF birden fazla etiketle + switch/case/break |

**RETURN / EXIT**

| Test | Dogrular |
|------|----------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | FOR icinde EXIT → break |

### 1.7 Fonksiyon bloklari (FB cagrilari)

| Test | Dogrular |
|------|----------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — OUT => atamasi |

### 1.8 Dizi erisimi

| Test | Dogrular |
|------|----------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | FOR dongusunde dizi erisimi |

### 1.9 Tur donusumleri

Derleyici `XXX_TO_YYY` kalibini tanir ve IEC standardina uygun
C tarzi donusumler (`(TYPE)value`) uretir.

| Test | ST Kodu | Uretir |
|------|---------|--------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 Yapi uyesi erisimi

| Test | Dogrular |
|------|----------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 Gorevler arasi degiskenler (coklu gorev)

| Test | Dogrular |
|------|----------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` kilitsiz okuma icin |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` kilitsiz yazma icin |
| `crossStructuredGet` | `__snap_` is parcacigi yerel snapshot erisimi |
| `crossStructuredMemberAccess` | `__snap_Struct.field` erisimi |

### 1.12 Standart fonksiyon bloklari

Her IEC standart FB bir ornek olarak olusturulur ve cagrilir:

| Test | FB Turu | Dogrular |
|------|---------|----------|
| `fbTon` | TON | Acma gecikmesi |
| `fbTof` | TOF | Kapama gecikmesi |
| `fbTp` | TP | Darbe zamanlayicisi |
| `fbCtu` | CTU | Yukari sayici |
| `fbCtd` | CTD | Asagi sayici |
| `fbRtrig` | R_TRIG | Yukselen kenar |
| `fbFtrig` | F_TRIG | Dusen kenar |
| `fbRs` | RS | Reset-baskin |
| `fbSr` | SR | Set-baskin |

### 1.13 Standart fonksiyonlar

| Kategori | Testler | Fonksiyonlar |
|----------|--------:|--------------|
| Matematik | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| Secim | 4 | SEL, LIMIT, MIN, MAX |
| Karakter dizisi | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| Bit kaydirma | 4 | SHL, SHR, ROL, ROR |
| Tur donusumu | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 Sinir durumlar

| Test | Dogrular |
|------|----------|
| `complexNestedExpression` | Ic ice ifadeler |
| `multipleStatementsOnSeparateLines` | Cok satirli programlar |
| `emptyBody` | Bos POU govdesi |
| `commentOnlyBody` | Yalnizca yorumlar |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | Buyuk/kucuk harf duyarliligi |

---

## 2. Standart kutuphane (FStLibraryTest)

8 veri odakli test, standart kutuphanedeki (`standard_library.sql`)
**tum 132 bloku** otomatik olarak dogrular.

### 2.1 Fonksiyon bloklari (13 FB)

| Test | Dogrular |
|------|----------|
| `fbSingleInstance` | Her FB tek basina orneklenebilir ve cagrilabilir |
| `fbDoubleInstance` | Ayni FB turunun iki ornegi esanli |
| `fbOutputRead` | Tum cikislar cagri sonrasi okunabilir |

**Kapsanan FB'ler:** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 Fonksiyonlar (119 FC)

| Test | Dogrular |
|------|----------|
| `fcCall` | Her FC dogru parametrelerle cagrilabilir (104 test edildi) |
| `fcInExpression` | FC donus degeri ifadelerde kullanilabilir |

**Kapsanan kategoriler:**

- **Aritmetik:** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **Karsilastirma:** EQ, NE, LT, GT, LE, GE
- **Trigonometri:** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **Logaritma:** EXP, LN, LOG, SQRT
- **Secim:** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **Karakter dizisi:** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **Bit kaydirma:** SHL, SHR, ROL, ROR
- **Tur donusumu:** 60+ donusum fonksiyonu (BOOL_TO_INT, INT_TO_REAL, ...)
- **ForgeIEC uzantilari:** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. Coklu gorev (FCodeGeneratorThreadingTest)

8 test, tasarim spesifikasyonuna (MT-spec, docs/design/multi-task-scheduler.md)
uygun olarak tam coklu gorev zamanlama sistemini dogrular.

| Test | Dogrular |
|------|----------|
| `singleProgramDefaultTask` | Acik gorevi olmayan bir PROGRAM → DefaultTask sentezi, is parcacigi yok |
| `twoProgramsTwoTasks` | Iki gorev → RESOURCE0_start__, Legacy-Shim config_run__, her iki gorev is parcacigi |
| `crossPrimitiveAtomicEmission` | Paylasilan INT degiskeni → `std::atomic<>` Location depolamasi, govdede `__GET_EXTERNAL_ATOMIC` |
| `crossStructuredDoubleBuffer` | Paylasilan STRUCT → `__DBUF_[2]` + `thread_local __snap_` + Double-Buffer giris/cikis kopyasi |
| `localVarNoSync` | Yalnizca bir gorevdeki degisken → normal `__SET_EXTERNAL`, Atomic yok |
| `conflictTwoWriters` | Iki gorev ayni degiskene yazar → derleme uyarisi |
| `singleProgramDefaultTask` | Geriye uyumluluk: mevcut projeler degisiklik olmadan calisir |

### Coklu gorev mimarisi

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [bufferLock altinda]          | [lock-free]
```

**Senkronizasyon mekanizmalari:**
- **CrossPrimitive** (BOOL, INT, REAL, ...): Location degiskeni uzerinde `std::atomic<T>`, govde kodunda `__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC`
- **CrossStructured** (STRUCT, ARRAY, STRING): Atomik yazma indeksli Double-Buffer `__DBUF_[2]`, Set tutarliligi icin `thread_local` snapshot'lar `__snap_`

---

## Kalite guvencesi

### Otomatik dogrulama

Testler her derlemede `-DBUILD_TESTS=ON` ile calistirilir.
CI hattina (Forgejo Actions) entegrasyon hazirlanmistir.

### Veri odakli testler

Kutuphane testleri (`FStLibraryTest`) blok tanimlarini dogrudan
`standard_library.sql` dosyasindan okur. Yeni bloklar eklendiginde
otomatik olarak test edilir — manuel test senaryosu olusturmaya gerek yoktur.

### Tamlık

Test paketi, ForgeIEC tarafindan desteklenen IEC 61131-3 Structured Text
dil dagarcigininin tamamini kapsar:

- Tum operatorler (aritmetik, karsilastirma, mantiksal, bit kaydirma)
- Tum kontrol yapilari (IF, FOR, WHILE, REPEAT, CASE)
- Tum deger turleri (Integer, Real, Bool, String, Time)
- Tum standart FB ve FC'ler (132 blok)
- Dizi ve yapi erisimi
- GVL nitelikli degiskenler
- Gorevler arasi senkronizasyon (Atomics + Double-Buffer)
- Tur donusumleri (C donusum uretimi)
