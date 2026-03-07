---
title: "Tongs"
description: "Saha Veri Yolu Kopruleri -- Modbus, EtherCAT, Profibus"
weight: 6
---

## Tongs -- Saha Veri Yolu Kopruleri

Maşa, demircinin kizgin metali tutmak icin kullandigi alettir. **Tongs**,
saha cihazlarindan verileri yakalar ve PLC calisma zamanina tasir. Her saha
veri yolu protokolunun kendi koprusu vardir ve bagimsiz bir suerec olarak
calisir.

---

## Desteklenen Protokoller

### Modbus TCP

Modbus cihazlari icin Ethernet iletisimi. Register, bobin ve ayrik girislerin
okunmasi ve yazilmasi. Otomatik cihaz kesfetme icin entegre ag tarayicisi.

| Ozellik | Deger |
|---------|-------|
| Tasima | TCP/IP (Ethernet) |
| Kopru | `tongs-modbustcp` |
| Fonksiyon Kodlari | FC1, FC2, FC3, FC4, FC5, FC6, FC15, FC16 |
| Durum | Mevcut |

### Modbus RTU

RS-485 uzerinden Modbus cihazlari icin seri iletisim. Modbus TCP ile ayni
fonksiyonlar, seri tasimaya uyarlanmistir.

| Ozellik | Deger |
|---------|-------|
| Tasima | Seri RS-485 |
| Kopru | `tongs-modbusrtu` |
| Durum | Mevcut |

### EtherCAT

Suruculer, servo motorlar ve yuksek performansli G/C modulleri icin gercek
zamanli Ethernet saha veri yolu.

| Ozellik | Deger |
|---------|-------|
| Tasima | Ethernet (gercek zamanli) |
| Kopru | `tongs-ethercat` |
| Durum | Gelistirmede |

### Profibus DP

Mevcut tesislerde saha cihazlariyla iletisim icin kanitlanmis endustriyel
standart.

| Ozellik | Deger |
|---------|-------|
| Tasima | RS-485 / Fiber optik |
| Kopru | `tongs-profibus` |
| Durum | Gelistirmede |

---

## Mimari

Her kopru, `anvild` daemon'u tarafindan yonetilen bagimsiz bir suerec olarak
calisir. Calisma zamani ile iletisim Anvil (Sifir Kopyalama IPC) uzerinden
gerceklesir. Bir koprunun cokmesi ne PLC'yi ne de diger kopruleri etkiler.

```
anvild
  |
  +-- tongs-modbustcp --segment mb1 --> Modbus TCP Cihazlari
  |
  +-- tongs-modbusrtu --segment mb2 --> Modbus RTU Cihazlari
  |
  +-- tongs-ethercat  --segment ec1 --> EtherCAT Cihazlari
  |
  +-- tongs-profibus  --segment pb1 --> Profibus Cihazlari
```

### Suerec Yonetimi

- Calisma zamani baslatildiginda koprulerin otomatik baslatilmasi
- Surekli izleme -- cokmede otomatik yeniden baslatma
- Aktif veri yolu segmenti basina bir suerec
- Kopru basina bagimsiz kayit

---

## Yapilandirma

Veri yolu segmentleri hedef sistemdeki `config.toml` dosyasinda
yapilandirilir. Her segment protokolu, ag arayuzunu ve bagli cihazlari
tanimlar.

### G/C Degiskenleri

Her cihaz giris ve cikis degiskenleri sunar:

- **Yon "in"** -- Cihazdan okuma (Subscribe)
- **Yon "out"** -- Cihaza yazma (Publish)
- Catismasiz otomatik IEC adres atamasi (%I, %Q)

---

<div style="text-align:center; padding: 2rem;">

**Tongs -- Saha verilerinizi yakalayan maşa.**

blacksmith@forgeiec.io

</div>
