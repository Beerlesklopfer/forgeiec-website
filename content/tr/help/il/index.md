---
title: "Instruction List Düzenleyici"
summary: "IL düzenleyici: CR yazmacı ile akümülatör tabanlı IEC 61131-3 dili"
---

## Genel Bakış

**Instruction List (IL)**, IEC 61131-3'ün assembler benzeri metin
dilidir ve tarihsel olarak beş IEC dilinin ilkidir. Programlar, tek
bir dahili **akümülatör yazmacını** — *Current Result* (`CR`) — manipüle
eden komut dizileridir. Her satır şu formdaki bir ifadedir:

```
[Label:] Operator [Modifier] [Operand] (* Comment *)
```

ve akümülatörden veya bir dış değişkenden okur veya bunlara yazar.

ForgeIEC'te IL, `FIlEditor` aracılığıyla düzenlenir — düzen ve
araçlar [ST düzenleyici](../st/) ile benzerdir.

## Düzenleyici düzeni

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (tree-sitter-instruction-list grammar) |
+----------------------------------------+
```

| Alan | İçerik |
|---|---|
| **Değişken tablosu** (üst) | Name, Type, Initial value, Address, Comment ile tanımlamalar — `VAR ... END_VAR` bloğu ile senkronize. |
| **Kod alanı** (alt) | Tree-sitter vurgulamalı IL kaynağı (`tree-sitter-instruction-list` grameri). |
| **Arama çubuğu** (Ctrl-F / Ctrl-H) | Bul-değiştir çubuğu. |

Çevrimiçi mod ve satır içi değer yer paylaşımı, ST düzenleyiciyle aynı
şekilde çalışır.

## Akümülatör modeli

Akümülatör (`CR`), çalışan değerlendirmenin ara sonucunu tutar. Tipik
bir dizi:

  1. `LD x` — `x`'i akümülatöre yükle (`CR := x`)
  2. `AND y` — akümülatörü `y` ile birleştir (`CR := CR AND y`)
  3. `ST z` — akümülatörü `z`'ye depola (`z := CR`)

Bu, IL'yi **stack'siz, tek-yazmaçlı bir makine** yapar — dilin 1993'te
standartlaştırıldığı zamanlarda baskın olan mikrodenetleyici
platformlarına çok yakın.

## Temel operatörler

| Grup | Operatörler | Etki |
|---|---|---|
| **Yükle / Depola** | `LD`, `LDN`, `ST`, `STN` | Akümülatörü ayarla / akümülatörü depola (`N` = negatif) |
| **Set / Reset** | `S`, `R` | Bit ayarla / sıfırla (`CR` = TRUE olduğunda BOOL değişken) |
| **Bit mantığı** | `AND`, `OR`, `XOR`, `NOT` | Akümülatörü işlenenle birleştir |
| **Aritmetik** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` | Akümülatör + işlenen → akümülatör |
| **Karşılaştırma** | `GT`, `GE`, `EQ`, `NE`, `LE`, `LT` | Karşılaştırma sonucu `CR`'ye |
| **Atlama** | `JMP`, `JMPC`, `JMPCN` | Etikete atla (`C` = `CR` = TRUE olduğunda) |
| **Çağrı** | `CAL`, `CALC`, `CALCN` | Fonksiyon-blok örneği çağır |
| **Geri dönüş** | `RET`, `RETC`, `RETCN` | POU'dan çık |

## Değiştiriciler

Bir operatör son ek değiştiricileri aracılığıyla rafine edilebilir:

| Değiştirici | Anlam |
|---|---|
| `N` | İşlenenin **negasyonu** (`LDN x`, `NOT x`'i yükler) |
| `C` | **Koşullu** — yalnızca `CR` = TRUE olduğunda gerçekleştir (`JMPC label`) |
| `(`...`)` | **Parantez değiştiricisi** — `)` kapanana kadar değerlendirmeyi ertele |

Parantez formu, ara değişkenler olmadan bileşik ifadeleri etkinleştirir:

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## ST yerine IL'yi ne zaman kullanmalı

ST bugün varsayılan seçimdir. IL hâlâ şu durumlarda mantıklıdır:

  - **Mikrodenetleyici performansı** belirleyici olduğunda — IL,
    çoğu matiec arka ucunda makine komutlarına 1:1 eşlenir, ara
    optimizasyon olmadan.
  - **Eski sistemlerin** uyumlu tutulması gerektiğinde (S5/S7 AWL
    türevi mantık, eski ABB / Beckhoff kurulu taban).
  - **Çok kompakt mantık blokları** — kilitlemeler, mandallar, kenar
    koşulları genellikle IL'de ST'den iki satır daha kısadır.

Diğer her şey için ST daha okunabilir ve bakımı daha kolaydır.

## Kod örneği — NO/NC kontaklı kendinden tutmalı konaktör

IL'de klasik **konaktör kendinden tutma**: `start`'a basmak konaktör
`K1`'i enerjilendirir, `stop` butonu (NC, düşük aktif) onu tekrar
düşürür. Mantık:

```
K1 := (start OR K1) AND NOT stop
```

IL'de:

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

Dört komut, bir yazmaç, geçici depolama yok. Tam olarak IL'nin
başlangıçta tasarlandığı türden bir yapı.

## İlgili konular

- [Structured Text](../st/) — Pascal benzeri kardeş dil
- [Kütüphane](../library/) — `CAL` üzerinden çağrılabilir fonksiyon blokları
- [Proje dosya formatı](../file-format/) — `<body><IL>...` içindeki IL gövdesi
