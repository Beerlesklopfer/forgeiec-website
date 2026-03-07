---
title: "Anvil"
description: "Sifir Kopyalama IPC ile gercek zamanli PLC calisma zamani"
weight: 2
---

## Anvil -- Dovmenin Kalbi

Her demirci atolyesinde ors merkezi aractir -- burada metal sekil verilir,
sertlestirilir ve islenir. **Anvil**, PLC calisma zamani ile protokol
kopruleri arasindaki ara katmandir. Proses verileriniz burada dovulur:
alinir, donusturulur ve dogru alicilara dagitilir.

Anvil, surecler arasi iletisim icin tescilli bir sifir kopyalama paylasimli
bellek tasima katmani kullanir. Serializasyon yok, kopyalama yok, odun yok.

---

## Mimari

```
+--------------+         +------------+         +------------------+
|              |         |            |         |                  |
| PLC Programi |<------->|  anvild    |<------->|  Modbus Koprusu  |---> Saha Cihazlari
| (IEC Kodu)   |  gRPC   | (Daemon)   |  Anvil  |  EtherCAT Koprusu|---> Suruculer
|              |         |            |         |  Profibus Koprusu |---> Sensorler
+--------------+         +------------+         |  OPC-UA Koprusu  |---> SCADA
                                                +------------------+

                         <--- Anvil --->
                         Sifir Kopyalama IPC
                         Paylasimli Bellek
```

`anvild` ile protokol kopruleri arasindaki veri alisverisi **Anvil** uzerinden
gerceklesir -- sifir kopyalama paylasimli bellege dayali yuksek performansli
bir IPC kanali. Her segment kendi iletisim kanalini alir.

---

## Neden Anvil?

### Mikrosaniye Gecikmesi

Geleneksel IPC mekanizmalari (borular, soketler, mesaj kuyruklari) surecler
arasinda veri kopyalar. Anvil her kopyayi ortadan kaldirir. Veriler paylasimli
bellekte bulunur -- alici dogrudan okur.

| Yontem | Tipik Gecikme | Kopyalar |
|--------|--------------|----------|
| TCP Soketi | 50-200 us | 2-4 |
| Unix Soketi | 10-50 us | 2 |
| **Anvil** | **< 1 us** | **0** |

### Endustriyel Kalite

- Deterministik davranis -- kritik yolda dinamik bellek ayirma yok
- Kilitsiz algoritmalar -- engelleme yok, kilitlenme yok
- Yayinla/Abone ol modeli -- uretici ve tuketici arasinda gevsek baglanti
- Otomatik yasam dongusu yonetimi -- koprulerin izlenmesi ve cokme durumunda yeniden baslatilmasi

### IEC Programinda PUBLISH/SUBSCRIBE

Anvil, IEC 61131-3 programlamaya sorunsuz olarak entegre olur:

```iec
VAR_GLOBAL PUBLISH 'Motorlar'
    K1_Sebeke   AT %QX0.0 : BOOL;
    K1_Hiz      AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensorler'
    Sicaklik    AT %IW0   : INT;
    Basinc      AT %IW2   : INT;
END_VAR
```

PUBLISH/SUBSCRIBE anahtar kelimeleri, IEC 61131-3 standardina bir ForgeIEC
uzantisidir. Derleyici otomatik olarak Anvil baglamalarini olusturur.

---

## Desteklenen Protokoller

| Protokol | Kopru | Durum |
|----------|-------|-------|
| **Modbus TCP** | `tongs-modbustcp` | Mevcut |
| **Modbus RTU** | `tongs-modbusrtu` | Mevcut |
| **EtherCAT** | `tongs-ethercat` | Gelistirmede |
| **Profibus DP** | `tongs-profibus` | Gelistirmede |
| **OPC-UA** | `tongs-opcua` | Planlanmis |

Her kopru bagimsiz bir suerec olarak calisir. `anvild`, kopruleri otomatik
olarak baslatir, izler ve yeniden baslatir. Bir koprunun cokmesi ne PLC'yi
ne de diger kopruleri etkiler.

---

## Teknik Detaylar

- **IPC Cercevesi**: Anvil (tescilli sifir kopyalama paylasimli bellek)
- **Mimari**: Veri yolu segmenti basina bir yayinci/abone kanali
- **Veri Formati**: Ham IEC degiskenleri -- serializasyon yok, ek yuk yok
- **Platformlar**: x86_64, ARM64, ARMv7 (Linux)
- **Suerec Modeli**: Aktif segment basina bir kopru suereci

---

<div style="text-align:center; padding: 2rem;">

**Anvil -- Verilerin kontrol komutlarina dovuldugu yer.**

blacksmith@forgeiec.io

</div>
