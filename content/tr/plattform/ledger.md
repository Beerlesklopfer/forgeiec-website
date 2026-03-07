---
title: "Ledger"
description: "Uretim siparis yonetimi ve MES entegrasyonu"
weight: 7
---

## Ledger -- Uretim Siparis Yonetimi

**Gelistirme asamasinda**

Ledger, ForgeIEC platformunun uretim siparis yonetimi moduludur. Demircinin
defteri her uretilen parcayi kaydeder -- Ledger her uretim siparisini, her
uretim adimini ve her sonucu kaydeder.

---

## MES Entegrasyonu

MES (Uretim Yuruetme Sistemleri), uretim planlamasi (ERP) ile sahadaki
yuruetme (PLC'ler) arasindaki baglantidir. Ledger, ForgeIEC platformuna bu
entegrasyon katmanini saglayacaktir.

### Planlanan Ozellikler

- **Siparis Yonetimi** -- Uretim siparislerinin alinmasi, baslatilmasi ve takibi
- **Uretim Takibi** -- Parca sayimi, cekim sueresi, verimlilik orani
- **Izlenebilirlik** -- Her uretim partisine proses parametrelerinin iliskilendirilmesi
- **Uretim Raporlari** -- Vardiya, ekip veya doeneme goere otomatik rapor olusturma
- **ERP Arayuzu** -- Mevcut planlama sistemleriyle veri alisverisi

---

## Planlanan Mimari

Ledger, bagimsiz bir hizmet olarak calisacak, gercek zamanli proses verileri
icin Anvil (Sifir Kopyalama IPC) uzerinden calisma zamanina ve BT
sistemleriyle entegrasyon icin REST API uzerinden baglanacaktir.

### Platform Entegrasyonu

- **Anvil** -- Gercek zamanli proses verileri (sayicilar, makine durumlari)
- **Hearth** -- HMI'da uretim siparislerinin goruntuulenmesi
- **Bellows** -- Ucuncu taraf MES sistemleriyle OPC UA veri alisverisi
- **Forge Studio** -- IDE'den uretim degiskenlerinin yapilandirilmasi

---

## Kullanim Alanlari

### Ayrik Uretim

PLC sinyallerine dayali otomatik sayim ve hurda tespiti ile parca bazinda
uretim siparis takibi.

### Proses Endustrisi

Uretim partisi takibi, proses parametrelerinin (sicaklik, basinc, debi)
kaydi ve parti raporu olusturma.

### Bakim

Calisma saati sayicilari, oenleyici bakim doengueleri ve bakim siparislerinin
otomatik tetiklenmesi.

---

<div style="text-align:center; padding: 2rem;">

**Ledger gelistirme asamasindadir. Bilgiler proje ilerledikce
guncellenecektir.**

blacksmith@forgeiec.io

</div>
