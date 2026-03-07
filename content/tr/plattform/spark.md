---
title: "Spark"
description: "Zenoh Tuneli -- Edge-to-Cloud ag koeprusu"
weight: 5
---

## Spark -- Zenoh Tuneli

Spark, ForgeIEC platformunun Edge-to-Cloud ag koeprusudur. Kivilcim atesi
yakar -- Spark, sahadaki PLC'ler ile bulut hizmetleri arasindaki baglantiyi
atesler.

---

## Odunsuz Edge-to-Cloud

Modern endustriyel tesisler, saha ekipmanlari ile bulut hizmetleri arasinda
guvenilir bir baglantiya ihtiyac duyar -- uzaktan bakim, veri analizi ve
uzaktan izleme icin. Spark bu baglantiyi Zenoh protokolu uzerinden saglar.

### Neden Zenoh?

Zenoh, kisitli ve dagitik ortamlar icin tasarlanmis bir iletisim
protokoludur. Geleneksel VPN'ler veya MQTT baglantilarinin aksine Zenoh
sunlar sunar:

- **Yerel NAT Gecisi** -- Karmasik guvenlik duvari yapilandirmasi gerektirmez
- **Verimli pub/sub protokolu** -- Dusuk bant genisligi tuketimi
- **Uyarlanabilir yonlendirme** -- En iyi ag yolunun otomatik secimi
- **Minimum gecikme** -- Gercek zamanli uygulamalar icin tasarlanmistir

---

## Kullanim Alanlari

### Uzaktan Bakim

Uzak PLC'lere guvenli baglanti -- teshis, program guncelleme ve degisken
okuma. Sahaya gitme gerektirmez.

### Bulut Veri Toplama

Proses verilerinin bulut platformlarina (AWS, Azure, ozel altyapi) aktarimi
-- analiz, makine ogrenmesi ve ongorucu bakim icin.

### Coklu Tesis Izleme

Birden fazla tesisin tek bir noktadan merkezi izlemesi. Gercek zamanli
veriler ve minimum gecikme.

---

## Mimari

Spark, PLC uzerinde bir daemon olarak calisir ve Anvil (Sifir Kopyalama IPC)
uzerinden calisma zamanina baglanir. Veriler uzak Zenoh duguemlerine secici
olarak iletilir.

```
Tesis A                          Bulut / Merkez Tesis
+------------+                   +------------------+
| anvild     |                   | Zenoh Yonlendirici|
|   |        |                   |   |              |
|   +- Spark |----- Zenoh ---------|  +- Hizmetler  |
|   |  Anvil |   (sifreli)       |     Analitik     |
+------------+                   +------------------+
```

### Ozellikler

- Uctan uca sifreleme (TLS 1.3)
- Iletilen degiskenlerin yapilandirilaabilir filtrelemesi
- Ag kesintisinde otomatik yeniden baglanti
- Dusuk bant genislikli baglantilar icin veri sikistirma
- Mobil aglarla uyumluluk (4G/5G)

---

## Teknik Detaylar

- **Protokol**: Zenoh (zero overhead network protocol)
- **Tasima**: TCP, UDP, WebSocket
- **Sifreleme**: TLS 1.3
- **Platformlar**: x86_64, ARM64, ARMv7 (Linux)
- **Entegrasyon**: Calisma zamanina Anvil IPC, buluta Zenoh

---

<div style="text-align:center; padding: 2rem;">

**Spark -- Atolyeyi buluta baglayan kivilcim.**

blacksmith@forgeiec.io

</div>
