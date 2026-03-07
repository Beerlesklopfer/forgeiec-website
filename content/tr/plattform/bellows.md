---
title: "Bellows"
description: "Makineler arasi iletisim icin OPC UA Gecidi"
weight: 3
---

## Bellows -- OPC UA Gecidi

**Gelistirme asamasinda**

Bellows, ForgeIEC platformunun OPC UA gecididir. Demirci atolyesinin
korbasi atese hava verir -- Bellows, otomasyon sistemleri ile BT altyapisi
arasindaki iletisimi besler.

---

## Makineler Arasi Iletisim

OPC UA (Open Platform Communications Unified Architecture), Endustri 4.0
icin iletisim standardidir. Bellows, PLC degiskenlerini ust seviye
sistemlere sunan eksiksiz bir OPC UA sunucusu saglayacaktir.

### Ongorulen Kullanim Alanlari

- **SCADA Entegrasyonu** -- PLC'leri mevcut izleme sistemlerine baglama
- **M2M Veri Alisverisi** -- PLC'ler ile ucuncu taraf sistemler arasinda dogrudan iletisim
- **BT/OT Gecidi** -- Otomasyon aglari ile BT altyapisi arasinda kopru
- **Veri Arsivleme** -- Arsivleme icin proses verilerinin sunulmasi

---

## Planlanan Mimari

Bellows, `anvild` daemon'u tarafindan yonetilen bagimsiz bir suerec olarak
calisacaktir. Proses verileri Anvil (Sifir Kopyalama IPC) uzerinden alinir
ve OPC UA protokolu uzerinden sunulur.

```
PLC  --->  anvild  --->  Bellows (OPC UA Sunucusu)  --->  OPC UA Istemcileri
            Anvil IPC                                      SCADA, MES, Bulut
```

### Planlanan Ozellikler

- Spesifikasyona uygun OPC UA sunucusu
- IEC degiskenlerinin otomatik sunulmasi
- Yapilandirilaabilir bilgi modeli
- Sifreleme ve kimlik dogrulama
- Otomatik hizmet kesfi
- Entegre veri gecmisi

---

## Guvenlik

- Tum baglantilar icin TLS sifreleme
- Sertifika veya parola ile kimlik dogrulama
- Degisken bazinda ayrintili erisim kontrolu
- OPC UA guvenlik profillerine uyumluluk

---

<div style="text-align:center; padding: 2rem;">

**Bellows gelistirme asamasindadir. Bilgiler proje ilerledikce
guncellenecektir.**

blacksmith@forgeiec.io

</div>
