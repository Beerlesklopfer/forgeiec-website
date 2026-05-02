---
title: "Kütüphane (Fonksiyon Blokları + Fonksiyonlar)"
summary: "IEC 61131-3 standart kütüphanesi + ForgeIEC eklentileri + kullanıcı tanımlı bloklar"
---

## Genel Bakış

ForgeIEC kütüphanesi, bir uygulama programının `.forge` projesinden
çağırabileceği yeniden kullanılabilir tüm yapı taşlarının merkezi
koleksiyonudur — hem IEC 61131-3 ile standartlaştırılmış fonksiyon
blokları ve fonksiyonları hem de projeye özgü veya ForgeIEC'e özgü
eklentileri kapsar.

Kütüphane, **Kütüphane panelinde** (varsayılan dock: sağ kenar çubuğu)
gösterilir. Kütüphane paneli odaklıyken **F1**'e basarak bu sayfayı
açabilirsiniz.

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (project-specific blocks)
```

Kütüphane şu anda **neredeyse 100 blok** ve **30'un biraz üzerinde
fonksiyon** içermektedir. Her giriş şunları taşır:

  - **Ad** (örn. `TON`, `JK_FF`)
  - **Pin listesi** (tip ve konum ile birlikte girişler ve çıkışlar)
  - **Tip** (durum içeren `FUNCTION_BLOCK` veya durumsuz `FUNCTION`)
  - **Açıklama** + kullanım notları içeren **yardım metni**
  - **Kod örneği** (Kütüphane Yardım panelinde görünür)

## Kategori ağacı

### Standart Fonksiyon Blokları

| Grup | Bloklar |
|---|---|
| **Bistable** | `SR`, `RS` — öncelikli set/reset |
| **Edge Detection** | `R_TRIG`, `F_TRIG` — yükselen/düşen kenar |
| **Counters** | `CTU`, `CTD`, `CTUD` — yukarı / aşağı / her iki yönde sayım |
| **Timers** | `TON`, `TOF`, `TP` — açma gecikmesi / kapatma gecikmesi / darbe |
| **Motion** | profiller, rampalar, yörüngeler (hazırlık aşamasında) |
| **Signal Generation** | test ve doğrulama sinyalleri için üretici FB'ler |
| **Function Manipulators** | tutma, mandallama, geçmiş |
| **Closed-Loop Control** | PID, histerezis, iki-noktalı |
| **Application** *(ForgeIEC)* | `JK_FF`, `DEBOUNCE` — pratikte evrensel olarak yararlı bulunan uygulamaya yakın bloklar |

### Standart Fonksiyonlar

| Grup | İçerik |
|---|---|
| **Arithmetic** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` (herhangi bir ANY_NUM tipinde) |
| **Comparison** | `EQ`, `NE`, `LT`, `LE`, `GT`, `GE` |
| **Bitwise** | `AND`, `OR`, `XOR`, `NOT` (ANY_BIT üzerinde — bkz. `help/st`) |
| **Bit Shift** | `SHL`, `SHR`, `ROL`, `ROR` |
| **Selection** | `SEL`, `MAX`, `MIN`, `LIMIT`, `MUX` |
| **Numeric** | `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN` |
| **String** | `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND` |
| **Type Conversion** | `BOOL_TO_INT`, `REAL_TO_DINT`, `STRING_TO_INT`, ... |

### Kullanıcı Kütüphanesi

Projeye özgü tanımlı fonksiyon blokları ve fonksiyonlar — `FUNCTION_BLOCK`
veya `FUNCTION` olarak tanımlanan her şey otomatik olarak bu kategoride
yer alır ve standart bloklar gibi proje içinde her yerden çağrılabilir.

## Kütüphane paneli — kullanım

| Eylem | Etki |
|---|---|
| **Arama** (üstteki büyüteç) | Ağaç görünümünü blok adına göre filtreler — `to` yazmak `TON`'u bulur. |
| Bir bloğa **çift tıklama** | Detay bölmesinde blok yardımını açar: pin açıklamaları + kod örneği. |
| ST düzenleyiciye **sürükleme** | İmleç konumuna blok çağrısını ekler ve yerel `VAR_INST` bölümüne örnek tanımını ekler. |
| **Sağ tıklama > "Insert Call..."** | Sürükleme ile aynıdır, bağlam menüsü üzerinden. |
| Bir blokta **F1** | Bu sayfayı açar. |

## Örnek 1 — `DEBOUNCE` ile buton sıçrama önleme

`DEBOUNCE`, mekanik bir buton kontağındaki kısa gürültü darbelerini
filtreler. `Q` yalnızca `IN` tüm `T_Debounce` süresince stabil kaldıktan
sonra değişir — hem yükselen hem de düşen kenarlarda.

### Pin yerleşimi

| Pin | Yön | Tip | Anlam |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | Ham giriş (genellikle `%IX`, mekanik olarak sıçrayan) |
| `tDebounce`  | INPUT  | `TIME` | Minimum stabil süre (genellikle `T#10ms`...`T#50ms`) |
| `Q`          | OUTPUT | `BOOL` | Sıçrama önlenmiş çıkış |

### Kod örneği

`%IX0.0` üzerindeki bir basma butonunda sıçrama önleme yapan ve
sıçrama önlenmiş sinyali kendinden tutmalı bir konaktöre tek atımlı
bir kenar olarak ileten PROGRAM gövdesi:

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

`DEBOUNCE` dahili olarak iki `TON` bloğundan (yüksek ve düşük yön)
oluşur — biri `Q`'yu yalnızca `T_Debounce` süresince aktif `IN`'den
sonra TRUE'ya, diğeri yalnızca `T_Debounce` süresince inaktif `IN`'den
sonra FALSE'a getirir. Bu, filtreyi simetrik yapar: ne basıldığında ne
de bırakıldığında kontak sıçraması bir glitch üretir.

> **Tipik kullanım:** mekanik basma butonları, limit anahtarları,
> kontak tabanlı sensörler. "Basma başına tek atım" için — yukarıdaki
> gibi — `Q`'dan sonra bir `R_TRIG` zincirleyin.

## Örnek 2 — Mod geçersiz kılma ile kendinden tutma (`JK_FF`)

`JK_FF`, dahili buton sıçrama önleme özelliğine sahip bir toggle
flipfloptur. `xButton`'un her stabil yükselen kenarında `Q`'yu TRUE
ve FALSE arasında çevirir — böylece basit bir basma butonu, uygulama
programının DEBOUNCE + R_TRIG + toggle mantığını elle bağlamasına
**gerek kalmadan** "açma/kapama" anahtarına dönüşür.

### Pin yerleşimi

| Pin | Yön | Tip | Anlam |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | Ham buton kontağı (sıçrayan) |
| `tDebounce`  | INPUT  | `TIME` | Sıçrama önleme süresi (genellikle `T#20ms`) |
| `J`          | INPUT  | `BOOL` | "Set" (aktifken `Q`'yu TRUE'ya zorlar) |
| `K`          | INPUT  | `BOOL` | "Reset" (aktifken `Q`'yu FALSE'a zorlar) |
| `Q`          | OUTPUT | `BOOL` | Mevcut durum |
| `Q_N`        | OUTPUT | `BOOL` | Negatif durum (`NOT Q`) |
| `xStable`    | OUTPUT | `BOOL` | `xButton` `tDebounce` süresince stabil olduğunda TRUE |

### Kod örneği

Üç butonlu bir lamba kontrolü: `T1` lambayı çevirir, `T_Mains` zorla
açar (örn. "her yerde ana ışık açık"), `T_Off` her şeyi zorla kapatır:

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

`J`/`K` girişlerinin doğruluk tablosu:

| `J` | `K` | Davranış |
|---|---|---|
| FALSE | FALSE | Her sıçrama önlenmiş basışta çevir |
| TRUE  | FALSE | Q := TRUE (set, çevirmeyi geçersiz kılar) |
| FALSE | TRUE  | Q := FALSE (reset, çevirmeyi geçersiz kılar) |
| TRUE  | TRUE  | tanımsız — kaçının |

`xStable`, "buton şu anda basılı tutuluyor" mantığını uygulamanıza
olanak tanır (örn. çevirme etkisinin oturmasını beklemek zorunda
kalmadan basışı görselleştiren bir LED).

## Editör ve PLC arasında kütüphane senkronizasyonu

Standart kütüphane iki yerde bulunur:

  - **Editör tarafı:** `editor/resources/library/standard_library.json`
    (Qt kaynak sistemi aracılığıyla `.exe` içinde derlenir).
  - **PLC tarafı:** anvild submodülü, aynı JSON dosyası, yüklenen C
    kaynakları üzerindeki `make` adımıyla dahil edilir.

**Kütüphane senkronizasyonu**, bağlantıda her iki sürümün SHA-256
karşılaştırmasını yapar. Sapma durumunda Output panelinde bir ipucu
görünür; tepki yapılandırılabilir:

  - `Preferences > Library > Auto-Push` kapalı (varsayılan):
    `Tools > Sync Library` üzerinden manuel push. Bir üretim çalışma
    zamanını eski bir editörden gelen yanlışlıkla yapılan üzerine
    yazmaya karşı korur.
  - `Preferences > Library > Auto-Push` açık: sapma otomatik bir push
    tetikler. Tek programcılı geliştirme kurulumlarında yararlıdır.

## ForgeIEC eklentileri

Aşağıdaki bloklar IEC 61131-3'te standartlaştırılmamıştır ancak pratikte
evrensel olarak yararlı bulundukları için standart kütüphanenin bir
parçası olarak gönderilir:

| Blok | Amaç |
|---|---|
| `JK_FF` | Dahili buton sıçrama önleme ile toggle flipflop (bkz. Örnek 2). |
| `DEBOUNCE` | Simetrik buton sıçrama önleme (bkz. Örnek 1). |

Bu bloklar *Standard Function Blocks / Application* altında bulunur ve
JSON kaynağında `isStandard: true` olarak işaretlenir, bu da onları
"silinemez" olarak işaretler (yani Kütüphane paneli üzerinden
yanlışlıkla kaldırılamazlar).

## Kullanıcı Kütüphanesine kendi bloklarınızı ekleme

Mevcut projedeki her `FUNCTION_BLOCK` ve `FUNCTION` tanımı otomatik
olarak **Kullanıcı Kütüphanesi** altında yer alır. Görünürlük zamanlaması:

  1. **Kütüphane panelinde:** POU'yu tanımlayıp kaydettikten hemen sonra.
  2. **Kod tamamlayıcıda (Ctrl-Space):** anında.
  3. **FBD/LD düzenleyicide blok olarak:** anında.
  4. **PLC üzerinde:** `Compile + Upload` sonrası.

Bir bloğu projeler arası yeniden kullanmak için, POU'yu
`File > Export POU...` üzerinden bir `.forge-pou` dosyası olarak verin
ve hedef projede içeri aktarın — proje kapsamı aşan bir "çalışma alanı
kütüphanesi" backlog'tadır.

## İlgili konular

- [Structured Text söz dizimi](../st/) — ST'de bir blok çağrısının
  nasıl göründüğü.
- [Function Block Diagram düzenleyici](../fbd/) — bir bloğun grafik
  olarak nasıl bağlandığı.
- [Variables Panel](../variables/) — adres havuzunun örneği nasıl gördüğü.
