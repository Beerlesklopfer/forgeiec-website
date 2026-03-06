---
title: "Anvil"
summary: "Verileriniz bizim oeruemuzde doevueluer"
---

## Oerues: Her Demirci Ocaginin Kalbi

Her demirci ocaginda oerues merkezi parcadir — metal burada sekillenir,
sertlestirilir ve islenir. **Anvil**, PLC calisma zamani ile saha yolu
koepruelerinin arasindaki ara katmandir. Proses verileriniz burada
doevueluer: alinir, doenuestuerueluer ve dogru alicilara dagitilir.

Anvil dahili olarak **IceOryx2** uezerine insa edilmistir — suerecler arasi
iletisim icin sifir-kopyali paylasimli bellek cercevesi. Serializasyon yok,
kopyalama yok, taviz yok.

---

## Mimari

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ PLC Programi │◄───────►│  forgeiecd  │◄───────►│  Modbus Koeprue  │──► Saha Cihazlari
│  (IEC Kodu)  │  gRPC   │  (Daemon)  │  Anvil  │  EtherCAT Koeprue│──► Sueruecueler
│              │         │            │ IceOryx2│  Profibus Koeprue │──► Sensörler
└──────────────┘         └────────────┘         │  OPC-UA Koeprue  │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         Sifir-Kopya IPC
                         Paylasimli Bellek
```

`forgeiecd` ile protokol koepruelerinin arasindaki veri degisimi **Anvil**
uezerinden gerceklesir — IceOryx2 paylasimli bellek tabanli yuesek
performansli bir IPC kanali.

---

## Neden Anvil?

### Mikrosaniye Gecikme

Geleneksel IPC mekanizmalari (pipe, soket, mesaj kuyruklari) suerecler
arasinda veri kopyalar. Anvil tuem kopyalamayi ortadan kaldirir.
Veriler paylasimli bellekte bulunur — alici dogrudan okur.

| Yoentem | Tipik Gecikme | Kopyalar |
|---------|--------------|----------|
| TCP Soket | 50–200 us | 2–4 |
| Unix Soket | 10–50 us | 2 |
| **Anvil (IceOryx2)** | **< 1 us** | **0** |

### Enduestri Kalitesi

- Deterministik davranis — kritik yolda dinamik bellek tahsisi yok
- Kilitsiz algoritmalar — engelleme yok, deadlock yok
- Publish/subscribe modeli — ueretici ve tueketici arasinda gevsek baglanti
- Otomatik yasam doenguesue yoenetimi — koeprueler izlenir ve coekme durumunda yeniden baslatilir

### IEC Programinda PUBLISH/SUBSCRIBE

```iec
VAR_GLOBAL PUBLISH 'Motors'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensors'
    Temperature AT %IW0   : INT;
    Pressure    AT %IW2   : INT;
END_VAR
```

---

## Desteklenen Protokoller

| Protokol | Koeprue | Durum |
|----------|---------|-------|
| **Modbus TCP** | `forgeiec-modbustcp` | Mevcut |
| **Modbus RTU** | `forgeiec-modbusrtu` | Mevcut |
| **EtherCAT** | `forgeiec-ethercat` | Gelistirme asamasinda |
| **Profibus DP** | `forgeiec-profibus` | Gelistirme asamasinda |
| **OPC-UA** | `forgeiec-opcua` | Planli |

Her koeprue bagimsiz bir suerec olarak calisir. `forgeiecd` koepruelerini
otomatik olarak baslatir, izler ve yeniden baslatir.

---

<div style="text-align:center; padding: 2rem;">

**Anvil — Verilerin kontrol komutlarina doevueldugu yer.**

blacksmith@forgeiec.io

</div>
