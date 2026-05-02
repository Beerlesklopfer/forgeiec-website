---
title: "Bus Cihazları"
summary: "Bir bus segmentinin içindeki bir cihazın yapılandırılması (Modbus slave, EtherCAT slave, ...)"
---

## Genel Bakış

Bir **bus cihazı**, **bir segment içindeki tek bir cihazdır** —
genellikle bir Modbus TCP slave (I/O bloğu, sürücü), bir EtherCAT slave
(servo eksen, I/O coupler), bir Profibus DP slave veya bir EtherNet-IP
adaptörü. Her cihaz için sorumlu köprü, bir mantıksal bağlantı sürdürür,
yapılandırılmış kayıtları yoklar ve verileri Anvil IPC grubu aracılığıyla
PLC çalışma zamanına yayınlar.

Bir cihaz **modüler** olabilir: bir bus coupler (slot 0) 1..N I/O
modülünü slot 1..N'de taşır. Genişleme yuvası olmayan kompakt cihazların
boş bir `modules` listesi vardır — değişkenler doğrudan slot 0'da bulunur.

## Bir cihazın alanları

Yapı tanımı (segmentin yanında) `editor/include/model/FBusSegmentConfig.h`
içinde bulunur. Bir cihaz, `.forge` projesinde `<fi:segment>` içinde
`<fi:device>` olarak kalıcı hale getirilir (bkz. [Bus Yapılandırması](../)).

### Kimlik + adresleme

| Alan | Tip | Anlam |
|---|---|---|
| `deviceId` | UUID | Stabil birincil anahtar — oluşturma sırasında otomatik üretilir. Hostname yeniden adlandırma ve IP değişikliğinde korunur, tüm değişken bağlamalarını stabil tutar. |
| `hostname` | string | Kullanıcı görünür etiket (`"Maibeere"`, `"Stachelbeere"`). DHCP-güvenli, ancak açıkça birincil anahtar **değildir**. |
| `ipAddress` | string (IP) | IP adresi (Modbus TCP / EtherNet-IP). IP'siz cihazlar için boş (EtherCAT slave'leri kendilerini bus konumu üzerinden tanımlar). |
| `port` | int | TCP portu. Varsayılan `502` (Modbus TCP). |
| `slaveId` | int | Modbus slave ID (1..247). Genellikle TCP üzerinden `1`. |
| `anvilGroup` | string | Köprü ve PLC çalışma zamanı arasında zero-copy taşıma için Anvil IPC grubu. Konvansiyon: `hostname` ile aynı ad. |
| `catalogRef` | string | Cihazı tanımlayan bir FDD katalog girişine isteğe bağlı referans (`"WAGO-750-352"`). |
| `description` | string | Serbest metin açıklaması (`"Bewaesserungsventil Sued"`). |

### Modüller (yuvalar)

| Alan | Tip | Anlam |
|---|---|---|
| `modules` | `FBusModuleConfig` listesi | Cihazın I/O modülleri. Slot 0 = coupler / kompakt cihaz, slot 1..N = genişleme modülleri. Modül başına: `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

### Cihaz başına geçersiz kılmalar

Bu alanlar — yalnızca **bu** cihaz için — segmentin karşılık gelen
değerlerini geçersiz kılar. `0` veya boş string *segmentten devral*
anlamına gelir. Özellikler panelinde *Advanced Overrides* bloğunun
altında bulunurlar, genellikle daraltılmış olarak.

| Alan | Tip | Anlam |
|---|---|---|
| `mac` | string `AA:BB:CC:DD:EE:FF` | Statik ARP / kimlik kontrolü için MAC adresi. DHCP cihazlarda IP hırsızlığına karşı korur. |
| `endianness` | enum | Çoklu kayıt değerleri için word/byte sırası: `"ABCD"` (big-endian, IEC varsayılanı), `"DCBA"` (word swap), `"BADC"` (byte swap), `"CDAB"` (byte + word swap). Boş = segmentten devral. |
| `timeoutOverrideMs` | int (ms) | Cihaz başına zaman aşımı. `0` = segment zaman aşımını kullan. |
| `retryCount` | int | İstek başına yeniden deneme sayısı. `0` = segment varsayılanı. |
| `connectionMode` | enum | `"always"` (TCP'yi döngüler arasında açık tut) veya `"on_demand"` (işlem başına yeniden bağlan). Boş = segment / köprü varsayılanı. |
| `gatewayOverride` | string (IP) | Cihaz, bağlama NIC'inden farklı bir alt ağda olduğunda cihaz başına ağ geçidi. |

### Cihaza özgü ayarlar

`settings` haritası (anahtar/değer), yalnızca bu cihaz veya cihaz tipi
için anlamlı olan değerleri taşır — örn. bir sürücünün eşik değeri veya
tercih edilen bir fonksiyon kodu.

## Düzenleme akışı

| Eylem | Etki |
|---|---|
| Bir cihaz düğümüne **tek tıklama** | `FPropertiesPanel` tüm alanları satır içi düzenleyiciler olarak gösterir — General bloğu (hostname, IP, port, slave ID, Anvil grubu), Override bloğu (MAC, zaman aşımı, yeniden denemeler, endianness, bağlantı modu, ağ geçidi geçersiz kılma, açıklama) ve durum tablosu. |
| Bir cihaz düğümüne **çift tıklama** | Aynı alan kümesi ile modal `FBusDeviceDialog`'u açar. Düzenleme modunda, sonradan yapılan bir FDD içeri aktarımının mevcut I/O değişken bağlamalarını sessizce üzerine yazamaması için "Import from catalog" butonu kilitlidir. |

## Durum değişkenleri (salt okunur)

Çalışma zamanında her cihaz, daemon'un gRPC durum akışı üzerinden
gönderdiği bir durum yapısı yayınlar. Bu değerler özellikler panelinde
**salt okunur tablo** olarak gösterilir ve UI'dan **düzenlenemez** —
köprü onları yazar. ST kodundan bunlar yine de
`anvil.<seg>.<dev>.Status.*` altında nitelikli yollar olarak adreslenebilir:

| Durum değişkeni | Tip | Anlam |
|---|---|---|
| `xOnline` | `BOOL` | Cihaz şu anda erişilebilir (son istek yanıtlandı). |
| `eState` | `INT` | Durum enum: 0=offline, 1=connecting, 2=online, 3=error. |
| `wErrorCount` | `WORD` | Köprü başlangıcından itibaren başarısız istek sayacı. |
| `sLastErrorMsg` | `STRING` | Son hata mesajı (zaman aşımı, Modbus istisnası, ...). |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## Örnek: İki yuvalı WAGO 750 bus coupler

Slot 1'de bir 8-DI modülü (750-430) ve slot 2'de bir 8-DO modülü
(750-530) bulunan bir Modbus TCP bus coupler 750-352:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

8 giriş, adres havuzunda `deviceId="0e5d5537-..."`, `moduleSlot=1` ve
`modbusAddress=0..7` ile `%IX0.0..%IX0.7` olarak görünür. 8 çıkış
benzer şekilde `moduleSlot=2` ile.

## İlgili konular

* [Bus segmentleri](../segments/) — cihazın yaşadığı ağ.
* [Bus yapılandırması — şema genel bakışı](../) — XML kalıcılığı.
* [Proje dosya formatı](../../file-format/) — adres havuzu ve
  değişken-cihaz bağlamaları.
