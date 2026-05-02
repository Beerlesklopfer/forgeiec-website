---
title: "Ladder Diagram Düzenleyici (LD)"
summary: "Devre şeması metaforu: güç rayları, kontaklar, bobinler"
---

## Genel Bakış

Ladder Diagram (LD), üç grafik IEC 61131-3 dilinin en eskisidir ve
**devre şeması metaforunu** izler: bir sol ve bir sağ **güç rayı**
arasında, yatay **akım yolları** (basamaklar) sinyali taşır. Her
basamakta kontaklar solda (seri olarak) ve bobinler sağda yer alır;
değişken durumuna bağlı olarak akımı ya "geçirirler" ya da "engellerler".
LD, basit kontrol mantığı için iyi bir seçimdir — limit anahtarları,
mandallama devreleri, kilitlemeler — ve elektrik planlamacıları için
oldukça okunabilirdir.

## Düzenleyici düzeni

LD düzenleyicisi, FBD düzenleyicisi ile aynı yapıya sahiptir (üstte
araç çubuğu, ızgara + zoom + pan ile QGraphicsView, sağda değişken
tablosu) ve iki özelliği vardır:

* **Sol güç rayı** ve **sağ güç rayı** diyagramda kalıcı öğelerdir.
  Taşınamazlar ve basamak sayısı ile dikey olarak büyürler.
* Araç çubuğu, LD sembolleri (kontaklar, bobinler, kenar tetikleyicileri)
  için butonlar ve güç rayları arasına yeni bir basamak bağlantısı
  ekleyen bir `Add Rung` butonu ekler.

## Semboller

### Kontaklar (basamağın sol tarafı)

| Sembol | Anlam |
|---|---|
| `--\| \|--` | **NO kontak** — değişken TRUE olduğunda geçirir |
| `--\|/\|--` | **NC kontak** — değişken FALSE olduğunda geçirir |
| `--\|P\|--` | **Yükselen kenar kontağı** — yükselen kenarda bir döngü için geçirir |
| `--\|N\|--` | **Düşen kenar kontağı** — düşen kenarda bir döngü için geçirir |

Seri kontaklar mantıksal **AND** olarak, paralel yollar mantıksal **OR**
olarak hareket eder.

### Bobinler (basamağın sağ tarafı)

| Sembol | Anlam |
|---|---|
| `--( )` | **Standart bobin** — mevcut yol durumunu değişkene yazar |
| `--(/)` | **Negatif bobin** — ters durumu yazar |
| `--(S)` | **Set bobini** — değişkeni TRUE'ya ayarlar ve mandallar (yol daha sonra açılsa bile) |
| `--(R)` | **Reset bobini** — değişkeni FALSE'a ayarlar ve mandallar |

Set/reset çiftleri, açık IF-THEN mantığı olmadan bir mandallama devresi
uygular.

### Basamakta fonksiyon blokları

Kütüphaneden fonksiyonlar ve fonksiyon blokları, **kontaklar ve
bobinler arasında satır içi** olarak eklenebilir. LD düzenleyici onları
sağda ve solda pin listeleri olan yatay bir kutu olarak çizer —
anlamsal olarak FBD bloğu ile aynıdır. Tipik kullanımlar: zamanlayıcılar
(`TON`), sayaçlar (`CTU`), karşılaştırıcılar (`GT`, `EQ`).

## Örnek — durdurma önceliğine sahip mandallama devresi

Klasik bir röle devresi: bir başlat butonu `xStart` bir motor `qMotor`'u
açar, bir durdurma butonu `xStop` onu kapatır. `xStart` en az bir kez
basılı olduğu ve `xStop` basılı olmadığı sürece motor açık kalır
(kendinden tutmalı).

```text
        |                                              |
        |   xStart      xStop                          |
   +----| |---+--|/|---+-----------------------( )----+
        |    |         |                       qMotor  |
        |    |         |                                |
        |   qMotor     |                                |
        +----| |-------+                                |
        |                                              |
```

Bir cümle olarak okuyun:

  * `xStart` (NO) **veya** `qMotor` (kendinden tutma kontağı, NO) — paralel olarak,
  * **ve** `xStop` (NC) — seri olarak,
  * `qMotor` bobinini sürer.

Derleme zamanında LD derleyici bu basamağı şuna çevirir:

```text
qMotor := (xStart OR qMotor) AND NOT xStop;
```

Bu, durdurma öncelikli bir mandalın en basit şeklidir. Her iki buton
aynı anda basılırsa, `xStop` kazanır çünkü NC kontağı yolu açar.

## İlgili konular

* [Function Block Diagram](../fbd/) — veri akışı odaklı kardeş dil.
* [Kütüphane](../library/) — basamakta satır içi kullanım için
  fonksiyon blokları (`TON`, `CTU`, `JK_FF`, `DEBOUNCE`).
* [Variables Panel](../variables/) — adres havuzu ve değişken bağlama.
