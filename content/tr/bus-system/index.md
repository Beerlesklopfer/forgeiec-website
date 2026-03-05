---
title: "Bus Sistemi"
summary: "ForgeIEC ile endüstriyel iletişim"
---

## Hiyerarşik Bus Sistemi Yönetimi

ForgeIEC, endüstriyel iletişimi CoDeSys uyumlu bir segment
hiyerarşisinde organize eder:

```
Bus Sistemleri
+-- Modbus TCP: Salon 1 (eth0) [aktif]
|   +-- 192.168.1.100 -- Sıcaklık Modülü (Slave 1)
|   |   +-- Sicaklik : INT (%IW0)
|   |   +-- Ayar_Degeri : INT (%QW10)
|   +-- 192.168.1.101 -- Pompa (Slave 2)
+-- Modbus RTU: Laboratuvar (/dev/ttyUSB0)
+-- Atanmamış (Tarayıcı Havuzu)
    +-- 192.168.2.55 -- Bilinmeyen
```

## Desteklenen Protokoller

| Protokol | Ortam | Kullanım Alanı |
|----------|-------|----------------|
| **Modbus TCP** | Ethernet | Bina otomasyonu, proses teknolojisi |
| **Modbus RTU** | RS-485 (seri) | Sensörler, basit alan cihazları |
| **EtherCAT** | Ethernet (gerçek zamanlı) | Hareket kontrolü, hızlı G/Ç |
| **Profibus DP** | Seri (alan veriyolu) | Üretim otomasyonu |

## Otomatik Adres Ataması

IEC adresleri (`%IX`, `%QW`, `%MD` vb.) global ve çakışmasız atanır.
Global değişken listelerindeki mevcut adresler dikkate alınır.

## Cihaz Keşfi

Entegre ağ tarayıcı, Modbus uyumlu cihazları otomatik olarak keşfeder.
Bulunan cihazlar doğrudan bir segmente atanabilir.

## Değişiklik İzleme

Bus değişkenlerindeki değişiklikler, çalışma zamanı sistemine aktarılmadan
önce açık bir fark diyaloğunda gösterilir. Kullanıcı tam kontrolü elinde tutar.
