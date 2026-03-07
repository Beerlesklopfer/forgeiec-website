---
title: "Forge Studio"
description: "IEC 61131-3 Gelistirme Ortami -- PLC programlama icin profesyonel IDE"
weight: 1
---

## Forge Studio -- Endustriyel Otomasyon IDE'si

Forge Studio, IEC 61131-3 standardina uygun PLC programlama icin ForgeIEC'in
entegre gelistirme ortamidir. C++17 ve Qt6 ile gelistirilmis olup, tum PLC
programlama gorevleri icin endustriyel kalitede bir arac sunar.

---

## Bes IEC 61131-3 Dili

Tum diller icin tek bir editor -- sorunsuz gecis, paylasimli degiskenler,
birlesik proje yapisi.

- **Yapilandirilmis Metin (ST)** -- Sozdizimi vurgulama, otomatik tamamlama, bul ve degistir
- **Komut Listesi (IL)** -- Akilli duzenleme ile tam dil destegi
- **Fonksiyon Blok Diyagrami (FBD)** -- Blok kutuphaneli grafik editor
- **Merdiven Diyagrami (LD)** -- Anahtarlama mantigi icin tanidik gosterim
- **Sirali Fonksiyon Seması (SFC)** -- Proses kontrolu icin adim sira diyagramlari

---

## Derleme ve Dagitim

Forge Studio, IEC programlarini is istasyonunda yerel olarak derler. Olusturulan
C dosyalari sifrelenmis gRPC uzerinden hedef PLC'ye aktarilir. PLC yalnizca
bir C derleyicisine ihtiyac duyar -- hedef sistemde IEC derleyicisi gerekmez.

- `iec2c` ile yerel derleme (IEC 61131-3'den C'ye)
- Hedef sisteme sifrelenmis aktarim
- Platforma uyarlanmis Makefile'in otomatik olusturulmasi
- x86_64, ARM64 ve ARMv7 mimarileri destegi

---

## Endustriyel Veri Yolu Sistemleri

CoDeSys tarzi saha veri yolu yapilandirmasi, segment hiyerarsisi ve otomatik
cihaz kesfetme.

- **Modbus TCP** -- Ethernet iletisimi
- **Modbus RTU** -- RS-485 seri baglanti
- **EtherCAT** -- Gercek zamanli Ethernet saha veri yolu
- **Profibus DP** -- Kanitlanmis endustriyel standart
- Catismasiz otomatik IEC adres atamasi
- Cihaz kesfetme icin ag tarayicisi

---

## Canli Hata Ayiklama

- PLC calisirken degiskenleri gercek zamanli izleme
- Uretim durdurmadan deger zorlama
- Filtreleme fonksiyonlu izleme paneli

---

## Standart Kutuphane

Eksiksiz IEC standart kutuphanesi: sayicilar, zamanlayicilar, kenar algilama,
tip donusumleri ve matematiksel fonksiyonlar. Kullanici tanimli bloklarla
genisletilebilir. Hizli erisim ve verimli arama icin SQLite veritabaninda
saklanir.

---

## Kullanici Yonetimi

- bcrypt sifreleme ile parola kimlik dogrulamasi
- Oturumlar icin JWT jetonlari
- CoDeSys tarzi ilk giris
- Role dayali erisim kontrolu

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio -- Endustri icin programlama. Acik Kaynak.**

blacksmith@forgeiec.io

</div>
