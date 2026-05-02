---
title: "Bus Segmentleri"
summary: "Bir alan veri yolu segmentinin yapılandırılması (bir arabirim üzerindeki bir fiziksel ağ)"
---

## Genel Bakış

Bir **bus segmenti**, **PLC hedefinin bir arabirimi üzerindeki bir
fiziksel ağı** tanımlar — genellikle Modbus TCP / EtherCAT / EtherNet-IP
için bir Ethernet portu (`eth0`, `enp3s0`) veya Modbus RTU / Profibus DP
için bir seri port (`/dev/ttyUSB0`). Her segment için, `anvild` daemon'u
**tam olarak bir köprü işlemi** (`tongs-modbustcp`, `tongs-ethercat`, ...)
başlatır ve bu işlem, o segmentteki tüm cihazlara giden trafiği yönetir.

Bir proje istediği kadar segment içerebilir — her biri kendi protokolü,
kendi arabirimi ve kendi yoklama frekansı ile. Örneğin hızlı bir EtherCAT
eksen denetleyicisi (`eth1`, 1 ms) ve yavaş bir Modbus TCP sensör
yoklayıcısı (`eth0`, 100 ms) aynı projede yan yana çalışabilir.

## Bir segmentin alanları

Yapı tanımı `editor/include/model/FBusSegmentConfig.h` içinde bulunur.
Bir segment, `.forge` projesinde `<fi:busConfig>` içinde `<fi:segment>`
olarak kalıcı hale getirilir (bkz. [Bus Yapılandırması](../)).

### Kimlik + protokol

| Alan | Tip | Anlam |
|---|---|---|
| `segmentId` | UUID | Stabil birincil anahtar — oluşturma sırasında otomatik üretilir, düzenlenemez. Ad değişikliği, protokol değişikliği ve IP değişikliğinde korunur. |
| `protocol` | enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Hangi köprü daemon'unun başlatılacağını belirler. |
| `name` | string | Kullanıcı etiketi (örn. `"Fieldbus Hall 1"`). Serbest formatlı, ağaçta ve loglarda gösterilir. |
| `enabled` | bool | Açma/kapama anahtarı. `false` = köprü başlatılmaz, cihazlar çevrimdışı kalır. Varsayılan: `true`. |

### Arabirim + yönlendirme

| Alan | Tip | Anlam |
|---|---|---|
| `interface` | string | Ağ arabirimi (`eth0`, `enp3s0`, `/dev/ttyUSB0`). Köprü tarafından soket / seri API'ye iletilir. |
| `bindAddress` | string (IP/CIDR) | Giden TCP bağlantıları için kaynak IP, örn. `192.168.24.100/24`. Boş = işletim sistemi arabirimin ilk IP'sini seçer. |
| `gateway` | string (IP) | Yerel alt ağı terk eden paketler için varsayılan ağ geçidi. Boş = ağ geçidi yok. |
| `pollIntervalMs` | int (ms) | Köprü yoklama aralığı. `0` = mümkün olduğu kadar hızlı (busy loop / gerçek zamanlı). Tipik: Modbus TCP için `100`, EtherCAT için `0`. |

### Ağ ayarları (gelişmiş)

Bu alanlar ağ ayarları sprintinde eklenmiştir ve işletim sistemi
varsayılanlarının yetersiz kaldığı durumları kapsar — tipik olarak: bir
slave başına çok sayıda paralel TCP bağlantısı, NAT üzerinden uzun süreli
TCP oturumları veya tek bir NIC üzerinde birden fazla alt ağ.

| Alan | Tip | Anlam |
|---|---|---|
| `subnetCidr` | string (CIDR) | Segmentin yerel alt ağı, örn. `192.168.24.0/24`. Bağlama NIC'i birden fazla ağ taşıdığında köprünün cihaz başına ağ geçidi geçersiz kılmalarını doğru şekilde yönlendirmesini sağlar. |
| `sourcePortRange` | string `"min-max"` | Giden bağlantılar için TCP kaynak port havuzu, örn. `30000-39999`. Boş = işletim sistemi ephemeral aralıktan seçer. Aynı slave'e çok sayıda paralel bağlantı gerektiğinde önemlidir (kaynak port başına bir bağlantı). |
| `keepAliveIdleSec` | int (s) | İlk TCP keep-alive sondası gönderilmeden önceki boşta kalma saniyeleri. `0` = işletim sistemi varsayılanı. |
| `keepAliveIntervalSec` | int (s) | Keep-alive sondaları arasındaki aralık. `0` = işletim sistemi varsayılanı. |
| `keepAliveCount` | int | Bağlantı ölü ilan edilmeden önceki başarısız sonda sayısı. `0` = işletim sistemi varsayılanı. |
| `maxConnections` | int | Bağlantı havuzunun üst sınırı. `0` = sınırsız. Sıkı bağlantı sınırı olan slave'lere karşı yararlıdır. |
| `vlanId` | int (1..4094) | Giden çerçeveler için 802.1Q VLAN etiketi. `0` = etiketsiz. |

### Protokole özgü ayarlar

`settings` haritası (anahtar/değer), yalnızca belirli bir protokol için
anlam taşıyan tüm değerleri tutar — örn. Modbus TCP için: `port`,
`timeout_ms`; Modbus RTU için: `serial_port`, `baud_rate`, `parity`,
`stop_bits`; Profibus için: `master_address`. `log_level` ve `log_file`
de aynı haritada protokolden bağımsız olarak tutulur.

## Düzenleme akışı

Bus ağacı panelinde her iki yol da eşdeğerdir — aynı alan kümesi
üzerinde işlem yaparlar ve aynı semantik etkiye sahiptirler:

| Eylem | Etki |
|---|---|
| Bir segment düğümüne **tek tıklama** | `FPropertiesPanel` (varsayılan dock: sağ taraf) tüm alanları satır içi düzenleyiciler olarak gösterir — değişiklikler `editingFinished` üzerinde projeye yazılır ve projeyi kirli olarak işaretler. |
| Bir segment düğümüne **çift tıklama** | Aynı alan kümesini *General* / *Modbus TCP* / *Advanced Network* / *Logging* olarak gruplandırılmış modal `FSegmentDialog`'u açar. OK kaydeder, Cancel iptal eder. |

## Örnek: Modbus TCP segmenti

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

Bu segment, kaynak IP `192.168.24.100` ile `eth0` üzerinde
`tongs-modbustcp`'yi başlatır, tüm cihazları her 100 ms'de bir yoklar
ve durum akışında bir zaman aşımı hatası yayınlanmadan önce istek başına
2000 ms'ye kadar yanıt süresi kabul eder.

## İlgili konular

* [Bus yapılandırması — şema genel bakışı](../) — XML kalıcılığı ve
  PLCopen `<addData>` mekanizması.
* [Bus cihazları](../devices/) — bir segment içindeki cihazlar.
* [Proje dosya formatı](../../file-format/) — `.forge` XML kökü.
