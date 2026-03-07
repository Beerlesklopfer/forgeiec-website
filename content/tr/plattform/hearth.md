---
title: "Hearth"
description: "Endustriyel proses gorsellestirme icin SCADA/HMI"
weight: 4
---

## Hearth -- SCADA/HMI

**Gelistirme asamasinda**

Hearth, ForgeIEC platformunun izleme ve insan-makine arayuzu sistemidir.
Ocak, demirci atolyesinin kalbidir, atesin yandigi yerdir -- Hearth, izlemenin
kalbidir, proseslerin gorsellestirildi yerdir.

---

## Proses Gorsellestirme

Endustriyel otomasyon sistemleri, uretim proseslerini gozlemlemek, kontrol
etmek ve teshis etmek icin bir izleme arayuzune ihtiyac duyar. Hearth bu
gorsellestirme katmanini saglayacaktir.

### Planlanan Ozellikler

- **Gercek Zamanli Panolar** -- Canli guncelleme ile proses degiskeni gorsellestirme
- **Proses Semalari** -- Endustriyel sembollerle tesislerin grafik gosterimi
- **Veri Gecmisi** -- Uzun vadeli egilim kaydi ve gosterimi
- **Alarm Yonetimi** -- Alarm algilama, bildirim ve onaylama
- **Raporlar** -- Otomatik uretim raporu olusturma

---

## Planlanan Mimari

Hearth bir web uygulamasi olarak calisacak ve agdaki herhangi bir
tarayicidan erisilebilir olacaktir. Proses verileri OPC UA (Bellows)
uzerinden veya dogrudan calisma zamanindan gRPC uzerinden alinacaktir.

### Planlanan Bilesenler

- Duyarli web arayuzu (masaustu ve tablet)
- Entegre proses semasi editoruu
- Yapilandirilaabilir alarm motoru
- Gecmis veritabani
- Kullanici yetkileri ve profil sistemi

---

## Platform Entegrasyonu

Hearth, ForgeIEC platformunun diger bilesenleriyle entegre olacaktir:

- **Anvil** -- Gercek zamanli proses verileri
- **Bellows** -- Standart OPC UA iletisimi
- **Ledger** -- Uretim verileri ve uretim siparisleri
- **Forge Studio** -- IDE'den yapilandirma

---

<div style="text-align:center; padding: 2rem;">

**Hearth gelistirme asamasindadir. Bilgiler proje ilerledikce
guncellenecektir.**

blacksmith@forgeiec.io

</div>
