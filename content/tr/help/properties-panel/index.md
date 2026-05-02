---
title: "Özellikler Paneli"
summary: "Proje ağacında seçilen bus elemanı için satır içi düzenleyici"
---

## Genel Bakış

**Properties paneli**, düzenleyicinin ana penceresinin sağ taraftaki
detay görünümüdür. **Proje ağacında şu anda seçili olan elemanın her
alanını** gösterir ve bu alanları satır içi düzenlenebilir hale getirir
— her düzenleme için bir modal diyalog açmaya gerek yoktur.

```
Project tree                          Properties panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- click   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

Bir ağaç düğümüne **tek tıklama**, eşleşen alan listesini hemen
görüntüler — **çift tıklama** ek olarak tam aynı alan kümesi ile modal
yapılandırma diyaloğunu ([Bus yapılandırması](../bus-config/)) açar.

Panel bir `QScrollArea` içine sarılmıştır ve dikey olarak kayar: FDD
eklentilerine sahip cihazlar artı durum tablosu kolayca 40+ alana
ulaşır ve dock dar olsa bile hepsinin erişilebilir kalması gerekir.

## Bus segmenti

Bir bus segmenti seçildiğinde panel şunları gösterir:

| Alan | Anlam |
|---|---|
| **Name** | Proje ağacındaki görünür ad. |
| **Protocol** | `modbustcp`, `modbusrtu`, `ethercat`, `profibus`, `ethernetip`. |
| **Interface** | Köprünün bağlandığı ağ arabirimi (`eth0`, `eth1`, …). |
| **Bind Address** | CIDR gösterimi, örn. `192.168.1.10/24`. Doğrulanır. |
| **Gateway** | Köprü işlemi için varsayılan ağ geçidi. |
| **Poll Interval** | Köprünün cihazlarını yokladığı `ms` cinsinden periyot. |
| **Enabled** | Köprü alt işleminin etkin olup olmadığı. |

### Advanced Network (tümü isteğe bağlı)

`FSegmentDialog`'daki aynı grubu yansıtır ve işletim sistemi / köprü
varsayılanlarını geçersiz kılar:

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count** (TCP heartbeat)
  - **Max Connections** (`0` = sınırsız)
  - **VLAN ID** (`0` = etiketsiz)

### Protokole özgü

| Protokol | Alanlar |
|---|---|
| `modbustcp`  | `Port` (varsayılan `502`), `Timeout` `ms` cinsinden (varsayılan `2000`). |
| `modbusrtu`  | `Serial Port` (örn. `/dev/ttyUSB0`), `Baud Rate`, `Parity` (`none`/`even`/`odd`). |
| `profibus`   | `Serial Port`, `Baud Rate` (12 Mbit/s'e kadar), `Master Address` (0..126). |

### Logging

  - **Log Level** — `off` / `error` / `warn` / `info` / `debug`.
  - **Log File** — örn. `/var/log/forgeiec/segment.log`. Boş = stdout.

## Bus cihazı

| Alan | Anlam |
|---|---|
| **Hostname** | DNS veya görünür ad. |
| **IP Address** | Cihazın IPv4'ü. |
| **Port** | Slave üzerindeki Modbus portu (varsayılan `502`). |
| **Slave ID** | Modbus birim ID'si (0..247). |
| **Anvil Group** | Anvil IPC grup adı — ayrıca otomatik üretilen `AnvilVarList`'in adı. Yeniden adlandırma, GVL etiketini, AnvilVarList'i ve `anvilGroup = oldGroup` olan her havuz değişkenini eşzamanlı olarak yeniden adlandırır. |

### Gelişmiş geçersiz kılmalar (tümü isteğe bağlı, boş = segmentten devral)

  - **MAC Address** — `AA:BB:CC:DD:EE:FF`. Doğrulanır.
  - **Endianness** — `ABCD` / `DCBA` / `BADC` / `CDAB`.
  - **Timeout** `ms` cinsinden. `0` = segmentten devral.
  - **Retry Count**. `0` = segmentten devral.
  - **Connection Mode** — `always connected` veya `on demand`.
  - **Gateway (override)** — yalnızca cihaz farklı bir alt ağda olduğunda.
  - **Description** — serbest metin (örn. `South irrigation valve`).

### Durum değişkenleri (salt okunur)

Her cihaz otomatik olarak ortak hata modelini açığa çıkarır — Anvil
üzerinden salt okunur bir durum konusu olarak yayınlanan yedi örtük alan:

| Ad | IEC tipi | Anlam |
|---|---|---|
| `xOnline`              | `BOOL`         | `eState = Online` veya `Degraded` olduğunda TRUE. |
| `eState`               | `eDeviceState` | Mevcut hata durumu. |
| `wErrorCount`          | `UDINT`        | Köprü başlatıldığından beri toplam hata sayısı. |
| `wConsecutiveFailures` | `UDINT`        | Son `Online`'dan beri başarısızlıklar (`Online`'da sıfırlanır). |
| `wLastErrorCode`       | `UINT`         | `0` = yok; `1..99` ortak; `100+` protokole özgü. |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8, sıfır ile doldurulmuş. |
| `tLastTransition`      | `ULINT`        | Son durum geçişinin Unix zamanı (ms). |

Cihaz `catalogRef` üzerinden bir **FDD**'ye (alan cihaz açıklaması)
bağlandığında, durum tablosu ek olarak FDD tarafından tanımlanan
eklentileri listeler ve `Source` sütununda `FDD +<offset>` olarak
işaretlenir.

ST kodunda her durum değişkeni `anvil.<seg>.<dev>.Status.*` olarak
erişilebilir:

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## Bus modülü

Bus modülleri bir cihazın içindeki I/O dilimleridir. Panel şunları gösterir:

### Meta veri

  - **Module** (görünür ad veya `catalogRef`)
  - **Slot** (cihaz içindeki slot indeksi)
  - **Catalog** (FDD referansı, örn. `Beckhoff.EL2008`)
  - **Base Addr** (IEC temel offseti)

### IO değişkenleri tablosu

`busBinding.deviceId` ve `busBinding.moduleSlot`'u bu modülle eşleşen
her havuz değişkenini listeler. Sütunlar:

| Sütun | İçerik |
|---|---|
| **Name** | Havuz adı (düzenlenebilir, örn. `Motor_Run`). |
| **Type** | IEC tipi (düzenlenebilir, örn. `BOOL`, `INT`). |
| **Address** | IEC adresi (`%IX0.0`, salt okunur). |
| **Bus Addr** | Modbus kayıt offseti (salt okunur). |
| **Dir** | `in` veya `out` (salt okunur). |

Sıralama düzeni: çıkışlardan önce girişler, ardından bus adresine göre
artan.

## Düzenleme davranışı

Paneldeki her düzenleme doğrudan modele karşı çalışır:

  1. Widget üzerinde düzenleme (`editingFinished` / `valueChanged` /
     `toggled`).
  2. Model alanı güncellenir (`seg->name = ...`).
  3. `project->markDirty()` kirli bayrağını yükseltir.
  4. `busConfigEdited` sinyali yayılır.
  5. Ana pencere gerekirse proje ağacı etiketini yeniler.

**Açık** bir `Apply` ve **açık** bir `Cancel` **yoktur** — düzenlemeler
hemen geçerli olur. Proje ağacında `Ctrl+Z` (geri al) son düzenlemeyi
geri alır.

## İlgili konular

  - [Bus yapılandırması](../bus-config/) — yüksek düzenleme hacmi olan
    güç kullanıcıları için aynı alan kümesine sahip modal diyaloglar.
  - [Variables paneli](../variables/) — `IO variables` tablosunu
    besleyen havuz.
