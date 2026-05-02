---
title: "Değişken ekleme"
summary: "FAddVariableDialog — tek bir modal içinde her alan, toplu oluşturma için aralık desenleri, dizi sarmalayıcısı"
---

## Genel Bakış

**FAddVariableDialog**, bir POU'ya veya havuza yeni bir değişken
eklemek için kullanılan modal penceredir. Tüm alanları tek bir adımda
toplar ve formun hemen altında ortaya çıkan IEC ST tanımının **canlı
önizlemesini** gösterir — yazdığınız şey anında bitmiş bir
`VAR ... END_VAR` parçacığı olarak görüntülenir.

Diyalog iki modda çalışır:

  - **Add modu**: boş alanlar, OK yeni bir değişken oluşturur.
    Variables panelindeki artı simgesi veya POU düzenleyicide Ctrl+N
    üzerinden erişilir.
  - **Edit modu**: paneldeki mevcut bir değişkene çift tıklayın — aynı
    diyalog, her alan önceden doldurulmuş olarak.

## Alanlar

| Alan | Zorunlu | Anlam |
|---|---|---|
| **Name** | evet | Programcı görünür adı. IEC tanımlayıcı kurallarına göre doğrulanır (harf + harfler/rakamlar/`_`). Aralık deseni ile toplu oluşturma için kullanılır (aşağıya bakın). |
| **Type** | evet | IEC temel tipleri, standart FB'ler, proje FB'leri, kullanıcı veri tipleri ile combo. Dizi oluşturma sarmalayıcı onay kutusu tarafından işlenir. |
| **Direction** | POU'ya bağlı | Değişken sınıfı — aşağıya bakın. |
| **Initial** | hayır | Başlangıç değeri (`FALSE`, `0`, `T#100ms`, `'OFF'`). |
| **Address** | hayır | Yalnızca VarList POU'ları için. Boş = oluşturma sırasında `pool->nextFreeAddress` otomatik tahsis eder. |
| **Retain** | hayır | Onay kutusu — RETAIN, değer güç döngüsünden sonra korunur. |
| **Constant** | hayır | Onay kutusu — `VAR CONSTANT`, çalışma zamanında yazılamaz. |
| **Array wrapper** | hayır | Seçilen tipi `ARRAY [..] OF` ile sarar. |
| **Documentation** | hayır | Serbest metin yorumu, PLCopen XML'inde `<documentation>` olarak saklanır. |

## Toplu oluşturma için aralık deseni

`LED_0`, `LED_1`, ... `LED_7`'yi tek tek yazmak yerine, ad alanında
**aralık deseni** belirtebilirsiniz:

| Giriş | Etki |
|---|---|
| `LED_0..7` | Sekiz değişken oluşturur: `LED_0` ile `LED_7` arası. |
| `LED_0-7` | Eşanlamlı, aynı etki. |
| `Sensor_1..3` | Üç değişken oluşturur: `Sensor_1` ile `Sensor_3` arası. |

Her toplu oluşturmada adres ayarlanmışsa artırılır:
`%QX0.0` → `%QX0.0`, `%QX0.1`, ..., `%QX0.7`.

## Dizi sarmalayıcı onay kutusu

Bir dizi olarak tanımlanmış **bir** değişken istiyorsanız dizi onay
kutusunu işaretleyin. İndeks aralığı için iki spin kutusu görünür ve
tip çalışma zamanında `ARRAY [..] OF <type>` olarak sarılır.

| Type combo | Array onay kutusu | İndeks aralığı | Sonuç tanımı |
|---|---|---|---|
| `INT` | kapalı | — | `: INT;` |
| `INT` | açık | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | açık | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor` (kullanıcı yapısı) | açık | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

Sarmalayıcı bilinçli olarak tip combo'su yerine bir onay kutusunda yer
alır — bu combo'yu dağınıklıktan korur ve combo'da arama yapmadan
herhangi bir şeyin dizilerini oluşturmanıza olanak tanır.

## Tip combo

Combo dört kaynağı tek bir listede toplar:

  1. **IEC temel tipleri**: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`,
     `INT`, `DINT`, `LINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`,
     `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
  2. Kütüphaneden **standart FB'ler**: `TON`, `TOF`, `TP`, `R_TRIG`,
     `F_TRIG`, `CTU`, `CTD`, `CTUD`, `SR`, `RS`, ...
  3. **Proje fonksiyon blokları** — mevcut projedeki her FB tanımı
     (kullanıcı kütüphanesi).
  4. `<dataTypes>` içinden **kullanıcı veri tipleri**: STRUCT'lar,
     enum'lar, takma adlar.

ARRAY şablonları combo'da görünmez — sarmalayıcı onay kutusundan geçerler.

## POU tipine göre yön (değişken sınıfı)

Hangi yön değerlerinin sunulacağı POU tipine bağlıdır:

| POU tipi | Mevcut yön |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | Sabit `VAR_GLOBAL` — combo gizlidir. |
| `AnvilVarList` | Sabit `VAR_GLOBAL` (otomatik üretilir) — combo gizlidir. |
| Havuz globalleri (POU konteyneri yok) | Yön yok — `%I`/`%Q` adresi onu örtük olarak ayarlar. |

## Düzenleme modu

Variables panelindeki mevcut bir değişkene çift tıklamak aynı diyaloğu
açar. Her alan önceden doldurulmuştur; OK'te değişiklikler
`pou->renameVariable` / `pool->rebind` üzerinden yönlendirilir
(`byAddress` indeksleri senkron kalır). Diyalog düzenleme modunu
`existing != nullptr` ile algılar.

## Örnek — Tek blokta 8 LED

Tek bir adımda havuz değişkenleri olarak sekiz çıkış LED'i:

  - **Name**: `LED_0..7`
  - **Type**: `BOOL`
  - **Direction**: gizli (havuz global)
  - **Address**: `%QX0.0` (otomatik artırma)
  - **Initial**: `FALSE`

OK sekiz havuz girişi oluşturur:

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

Sekiz değişken daha sonra Variables panelinde seçilebilir ve toplu
işlem yoluyla bir HMI grubuna atanabilir — örn.
`Set HMI Group... -> Frontpanel`.

## İlgili konular

  - [Değişken yönetimi](../) — sütunlar, filtreler ve toplu işlemler
    içeren Variables paneli.
  - [Proje dosya formatı](../../file-format/) — havuzun PLCopen XML'inde
    bir `<addData>` bloğu olarak nasıl kalıcı hale getirildiği.
