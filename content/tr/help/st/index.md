---
title: "Structured Text Düzenleyici"
summary: "ST düzenleyicisi + dil temelleri: IEC 61131-3 ifadeleri, bit erişimi, nitelikli havuz referansları"
---

## Genel Bakış

**Structured Text (ST)**, IEC 61131-3'ün Pascal benzeri yüksek seviyeli
dilidir ve ForgeIEC'te PROGRAM, FUNCTION_BLOCK ve FUNCTION POU'ları için
varsayılan düzenleyicidir. Düzenleyici, dikey bir splitter aracılığıyla
birleştirilmiş bir değişken tablosu ve kod alanından oluşan
`QWidget`-tabanlı bir kompozisyondur.

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

## Düzenleyici düzeni

| Alan | İçerik |
|---|---|
| **Değişken tablosu** (üst) | Name, Type, Initial value, Address, Comment sütunlarına sahip tanımlamalar. Düzenlemeler kodun `VAR ... END_VAR` bloğuna canlı senkronize edilir. |
| **Kod alanı** (alt) | Değişken bölümleri arasındaki ST kaynağı. Tree-sitter AST tarafından yönlendirilen satır katlama, satır numaraları, imleç satırı vurgusu. |
| **Arama çubuğu** (Ctrl-F / Ctrl-H) | Bul-değiştir modu ile kod alanının üzerinde gösterilir. |

Splitter, düzenleme durumunda POU başına konumunu hatırlar.

## Tree-sitter söz dizimi vurgulama

Regex tabanlı bir `QSyntaxHighlighter` yerine, ForgeIEC ST kaynağını
**Tree-sitter** ile bir AST'ye ayrıştırır ve capture sorguları aracılığıyla
renklendirir:

  - **Anahtar sözcükler** (`IF`, `THEN`, `FOR`, `FUNCTION_BLOCK`, ...): macenta
  - **Veri tipleri** (`BOOL`, `INT`, `REAL`, `TIME`, ...): camgöbeği
  - **Stringler + zaman literalleri** (`'abc'`, `T#20ms`): yeşil
  - **Yorumlar** (`(* ... *)`, `// ...`): gri, italik
  - **PUBLISH / SUBSCRIBE**: Anvil eklenti anahtar sözcükleri, özel stil

Avantaj: vurgulama karmaşık yapılarda doğru kalır (iç içe yorumlar, zaman
literalleri, nitelikli referanslar) ve aynı AST kod katlama için katlanabilir
aralıkları yönlendirir.

## Kod tamamlama (Ctrl-Space)

**Ctrl-Space**'e basmak veya iki eşleşen karakter yazmak tamamlama
açılır penceresini açar. Tamamlayıcı şunları bilir:

  - **IEC anahtar sözcükleri** (`IF`, `CASE`, `FOR`, `WHILE`, `RETURN`, ...)
  - **Veri tipleri** (`BOOL`, `INT`, `DINT`, `REAL`, `STRING`, `TIME`, ...)
  - Mevcut POU'nun **yerel değişkenleri**
  - Projedeki **POU adları** (PROGRAM, FUNCTION_BLOCK, FUNCTION)
  - **Kütüphane blokları** (`TON`, `R_TRIG`, `JK_FF`, `DEBOUNCE`, ...)
  - **Standart fonksiyonlar** (`ABS`, `SQRT`, `LIMIT`, `LEN`, ...)

Değişken havuzundaki değişiklikler (`poolChanged` sinyali) 100 ms debounce
ile tamamlama modeline yayılır — yeni havuz girişleri her tuş vuruşu tam
bir yeniden taramayı tetiklemeden neredeyse anında kullanılabilir hale gelir.

## Dil temelleri (IEC 61131-3)

### İfadeler

| İfade | Form |
|---|---|
| **Atama** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | Döngüden çık / POU'dan çık |

### Deyimler

IEC önceliği ile standart operatörler: `**`, tekli `+/-/NOT`, `* / MOD`,
`+ -`, karşılaştırmalar, `AND / &`, `XOR`, `OR`. Pascal'daki gibi
parantezler. Örtük sayısal tip dönüşümlerine izin verilmez —
`INT_TO_DINT`, `REAL_TO_INT` vb. açıkça çağrılmalıdır.

### ANY_BIT tiplerinde bit erişimi

`var.<bit>` doğrudan `BYTE`/`WORD`/`DWORD`/`LWORD` değişkenlerinde
tek bir biti ayıklar veya ayarlar:

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

Derleyici bunu yardımcı değişkenler olmadan `AND`/`OR`/shift ile temiz
bit maskeleme şekline çevirir.

### 3 seviyeli nitelikli referanslar

`<Category>.<Group>.<Variable>`, GVL'leri açıkça tanımlamak zorunda
kalmadan havuz girişlerine doğrudan erişir:

| Önek | Kaynak |
|---|---|
| `Anvil.X.Y`   | `anvilGroup="X"` olan havuz girişi |
| `Bellows.X.Y` | `hmiGroup="X"` olan havuz girişi |
| `GVL.X.Y`     | `gvlNamespace="X"` olan havuz girişi |
| `HMI.X.Y`     | `Bellows.X.Y` ile eşanlamlı |

`Anvil.X.Y` ve `Bellows.X.Y`, IEC adresleri farklı olduğu sürece bağımsız
olarak farklı havuz girişlerine işaret edebilir — derleyici ayrı C
sembolleri yayar.

### Konumlandırılmış değişkenler (`AT %...`)

Konumlandırılmış değişkenler bir tanımı bir IEC adresine bağlar:

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

Adres havuzdaki birincil anahtardır — bkz.
[Proje dosya formatı](../file-format/).

## Kod örnekleri

### Örnek 1 — Kütüphane bloğu ile TON çağrısı

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

`fbDelay`, kütüphane FB'si `TON`'un bir örneğidir. Tutulan
`start_button`'un 3 saniyesinden sonra `motor_run` TRUE'ya geçer.

### Örnek 2 — Bir çıkışı süren Bellows okuması

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` ve `Anvil.Sensors.contact_door`, derleyicinin
GVL tanımı olmadan çözdüğü 3 seviyeli referanslardır — her iki etiketin
de adres havuzunda tutulması ve `Pfirsich` grubu için HMI export'unun
aktif olması koşuluyla.

## İlgili konular

- [Kütüphane](../library/) — mevcut fonksiyon blokları + fonksiyonlar
- [Instruction List](../il/) — alternatif metin düzenleyici (akümülatör tabanlı)
- [Proje dosya formatı](../file-format/) — ST kodunun `.forge`'ta nasıl saklandığı
