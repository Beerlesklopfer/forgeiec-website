---
title: "Değişken Yönetimi"
summary: "FAddressPool üzerine merkezi görünüm olarak Variables paneli — sütunlar, filtreler, toplu işlemler, güvenlik anahtarları"
---

## Genel Bakış

**Variables paneli**, **FAddressPool** üzerine merkezi görünümdür — bir
ForgeIEC projesindeki her değişken için tek doğru kaynaktır. Her değişken
havuzda tam olarak bir kez bulunur, IEC adresine göre anahtarlanır
(`%IX0.0`, `%QW3`, ...). GVL, AnvilVarList, HmiVarList veya POU
arabirimleri gibi konteynerler yalnızca bu havuzun **görünümleridir** —
hiçbir değişken iki depoda paralel olarak yaşamaz.

```
FAddressPool  (single source of truth)
   |
   +-- FAddressPoolModel  (Qt table)
         |
         +-- FVariablesPanel  (filters + bulk ops + clipboard)
               |
               +-- Tree filter sets FilterMode + tag
```

Panel ana pencerenin altına dock olur ve her değişikliği anında diğer
tüm görünümlere yansıtır (POU düzenleyici, ST derleyici, PLCopen-XML
kaydı).

## Sütunlar

Tablonun **15 sütunu** vardır; her biri başlık bağlam menüsü üzerinden
ayrı ayrı açılıp kapatılabilir — her POU düzenleyici örneği sütun
görünürlüğünü bağımsız olarak saklar.

| Sütun | İçerik |
|---|---|
| **Name** | Programcı görünür adı. Nitelikli havuz girişleri tam yolları ile görünür: `Anvil.Pfirsich.T_1`, `Bellows.Stachelbeere.T_Off`, `GVL.Motor.K1_Mains`. |
| **Type** | IEC temel tipi veya kullanıcı tanımlı tip. Diziler `ARRAY [0..7] OF BOOL` olarak gösterilir. |
| **Direction** | IEC değişken sınıfı: POU yerelleri için `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP`; havuz globalleri için `in`/`out` (`%I` ve `%Q`'dan türetilir). |
| **Address** | IEC adresi — birincil anahtar. Bit girişi için `%IX0.0`, word çıkışı için `%QW1`, marker biti için `%MX10.3`. |
| **Initial** | Başlangıç değeri (`FALSE`, `0`, `T#100ms`, `'OFF'`). İlk döngüde değişkene yüklenir. |
| **Bus Device** | Bu değişkenin bağlı olduğu bus cihazının (Modbus slave vb.) UUID'si — açılır kutu olarak düzenlenebilir. |
| **Bus Addr** | Slave'e göreli Modbus kayıt offseti (`0`, `1`, ...). |
| **R** (Retain) | Onay kutusu — değer güç döngüsünden sonra korunuyor mu? |
| **C** (Constant) | Onay kutusu — IEC sabiti (`VAR CONSTANT`), değer çalışma zamanında yazılamaz. |
| **RO** (ReadOnly) | Onay kutusu — program kodundan salt okunur. |
| **Sync** | Çoklu görev senkronizasyon sınıfı (`L`/`A`/`D`), son ST derleyici çalışmasıyla üretilir. |
| **Used by** | Bu değişkeni hangi görevlerin okuduğu/yazdığı, örn. `PROG_Fast (R/W), PROG_Slow (R)`. |
| **Monitor** / **HMI** / **Force** | Değişken başına güvenlik anahtarları. Backlog'taki **Cluster A** — açık opt-in'ler, `hmiGroup` etiketinden farklı. ST derleyici codegen'den önce Force/HMI erişiminin yalnızca bayrağı taşıyan değişkenleri hedeflediğini doğrular. |
| **Live** | Çevrimiçi modda çalışma zamanı değeri (anvild canlı değer deposundan beslenir; bağlantı kesildiğinde gizlenir). |
| **Scope** | Osiloskop görünürlük onay kutusu — değişkeni kapsam paneline gönderir. |
| **Documentation** | Serbest metin yorumu. |

## Filtre modları

Panel havuzun tamamını aynı anda göstermez — **soldaki proje ağacı**
hangi dilimin görünür olacağını seçer. Bir ağaç düğümüne tıklamak ana
pencerenin `FilterMode` artı etiket ayarlamasını sağlar:

| FilterMode | Gösterir |
|---|---|
| `FilterAll` | Havuzun tamamı — etiket kısıtlaması yok. |
| `FilterByGvl` | `gvlNamespace == tag` olan değişkenler (örn. yalnızca `GVL.Motor`). |
| `FilterByAnvil` | `anvilGroup == tag` olan değişkenler (bir Anvil IPC grubu). |
| `FilterByHmi` | `hmiGroup == tag` olan değişkenler (bir Bellows HMI grubu). |
| `FilterByBus` | `busBinding.deviceId == tag` olan değişkenler (bir bus cihazının tüm değişkenleri). |
| `FilterByModule` | `FilterByBus` gibi, ayrıca `moduleSlot` — etiket formatı `hostname:slot`. |
| `FilterByPou` | POU yerelleri — `pouInterface == tag` olan değişkenler. |
| `FilterCommentsOnly` | Yalnızca yorum ayraçları, değişken yok. |

## Filtre eksenleri (birleştirilebilir)

Tablonun üstünde, ağaç filtresinin üzerine paralel olarak etki eden
dört ek eksen daha bulunur:

  - **Serbest metin araması** ad, adres ve etiketler üzerinde — `to`,
    `T_Off`'u bulur.
  - Combo olarak **IEC tipi filtresi** (`all` / `BOOL` / `INT` / `REAL` / ...).
  - **Adres aralığı filtresi**: `all` / `%I` (girişler) / `%Q` (çıkışlar) /
    `%M` (marker'lar); `%M` içinde word boyutuna göre daha fazla
    (`%MX` / `%MW` / `%MD` / `%ML`).
  - **TaggedOnly toggle** — herhangi bir konteyner etiketi olmayan her
    havuz girişini gizler ("yetim" bir havuzu bulmak için yararlıdır).

Her filtre AND ile birleştirilir: aktif olan tüm eksenlerle eşleşmeyen
hiçbir şey gizlenir.

## Çoklu seçim + toplu işlemler

Herhangi bir Qt tablosunda olduğu gibi: Shift-tıklama ve Ctrl-tıklama
aralıkları veya tek satırları seçer. Seçimdeki bağlam menüsü şunları sunar:

  - **Set Anvil Group...** — seçilen her değişkende `anvilGroup` ayarlar.
  - **Set HMI Group...** — `hmiGroup` için aynı.
  - **Set GVL Namespace...** — `gvlNamespace` için aynı.
  - **Clear Tag** — aktif filtre modunun etiketini temizler.
  - **Toggle Monitor / HMI / Force** — güvenlik anahtarlarının toplu
    olarak değiştirilmesi.

Her toplu düzenleme `FAddressPoolModel::applyToRows` üzerinden geçer,
tek bir `dataChanged` sinyaliyle sonuçlanır ve tek bir geri alma adımı
olarak geri alınabilir.

## Pano (kopyala / kes / yapıştır)

Seçilen değişkenler — **tüm etiketleri ve bayrakları ile** —
kopyalanabilir ve başka bir görünüme yapıştırılabilir. Yük iki format
kullanır:

  - Tam havuz bilgisini taşıyan dolaşım aracı olarak **Özel MIME**
    (`application/x-forgeiec-vars+json`).
  - Excel / metin düzenleyiciler için yedek olarak **TSV düz metin**.

**Yapıştırma** sırasında panel, konteyner etiketlerini otomatik olarak
**aktif filtre moduna** yeniden hedefler: `FilterByAnvil`'den (grup
`Pfirsich`) kopyalayın ve `FilterByHmi`'ye (grup `Stachelbeere`)
yapıştırın; değişkenler `anvilGroup`'larını bırakır ve
`hmiGroup = Stachelbeere` alır. Çakışan adresler ve adlar yinelemeden
arındırılır (`T_1` → `T_1_1`).

## HmiVarList'e sürükle/bırak

Değişkenler ana panelden bir HmiVarList POU'suna sürüklenebilir.
Editör daha sonra otomatik olarak değişkenin **HMI export bayrağını**
ayarlar ve HMI grubunu etiket olarak yazar — Bellows export artık
kullanıma hazırdır.

## Değişken başına güvenlik anahtarları

Her biri açık bir opt-in gerektiren değişken başına üç anahtar:

  - **HMI** — Bellows'un değişkeni okumasına/yazmasına izin verir.
  - **Monitor** — çevrimiçi modda canlı gözleme izin verir.
  - **Force** — bir çalışma zamanı değerini zorlamaya izin verir.

Bu bayraklar **`hmiGroup` etiketinden ayrıdır**. Etiket grup üyeliğini
tanımlar; bayrak etkiyi etkinleştirir. Her codegen'den önce ST
derleyici, her Bellows veya Force erişiminin bayrağı ayarlanmış bir
değişkeni hedeflediğini doğrular — aksi takdirde bir derleme hatası
oluşturur.

## İlgili konular

  - [Değişken ekleme](add/) — aralık desenleri ve dizi sarmalayıcısı
    olan `FAddVariableDialog`.
  - [Proje dosya formatı](../file-format/) — havuzun PLCopen XML'inde
    bir `<addData>` bloğu olarak nasıl kalıcı hale getirildiği.
  - [Kütüphane](../library/) — fonksiyon bloklarının havuzdaki
    örneklerini nasıl gördüğü.
