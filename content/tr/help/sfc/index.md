---
title: "Sequential Function Chart Düzenleyici (SFC)"
summary: "Sıralı kontrol ve mod makineleri için adım-geçiş modeli"
---

## Genel Bakış

Sequential Function Chart (SFC) üçüncü grafik IEC 61131-3 dilidir ve
bir adım-geçiş modeli aracılığıyla **durum yönelimli sıraları** tanımlar
— resmi olarak Petri ağları ile ilgilidir. Bir SFC diyagramı,
**koşullara sahip geçişlerle** bağlanan bir **adım** dizisinden oluşur.
Herhangi bir anda adımların bir alt kümesi aktiftir; bir adım, giden
geçişi TRUE olduğunda terk edilir.

SFC, **sıralı kontrol, mod makineleri ve toplu süreçler** için doğal
dildir — "önce bunu, sonra şunu, ... olduğu durumlar dışında" diye
tanımlayacağınız her şey.

## Düzenleyici düzeni

SFC düzenleyicisi, FBD ve LD ile aynı üç parçalı şemayı izler: üstte
araç çubuğu, ızgara + zoom + pan ile QGraphicsView, sağda değişken
tablosu. Araç çubuğu her SFC öğe tipi için araçlar sunar.

## Öğe tipleri

### Adım

Bir adım, bir ada sahip **dikdörtgen bir kutudur**. Aktif olduğu sürece,
onunla ilişkili eylemler çalışır.

* **Başlangıç adımı:** POU'nun giriş noktası. Program başlangıcında
  aktif olur. Düzenleyicide **çift kenarlıkla** çizilir.
* **Takip adımları:** Tek kenarlıkla çizilir. Önceki geçiş tetiklendiğinde
  aktif olurlar.

Portlar: üst (IN, önceki geçişten), alt (OUT, sonraki geçişe), sağ
(eylem bloklarına bağlantı).

### Geçiş

Bir geçiş, iki adım arasındaki dikey bağlantı çizgisinde **kısa yatay
bir çubuktur**. Çubuğun sağında **koşul** bulunur — ya bir ST ifadesi
(örn. `tmr.Q AND xReady`) ya da bir fonksiyon bloğunun çıkışı.

Koşul TRUE olduğunda, önceki adım deaktive olur ve takip eden adım
aktif hale gelir.

### Eylem bloğu

Bir eylem bloğu, **bir adım aktifken ne olacağını** tanımlar. İki
hücreden oluşur: solda **niteleyici** ve sağda **eylem adı** (bir ST
eylemine veya bir çıkış değişkenine referans).

| Niteleyici | Anlam |
|---|---|
| `N` | Saklanmamış — adım aktifken çalışır (varsayılan). |
| `P` | Darbe — adım aktivasyonunda bir döngü için bir kez tetiklenir. |
| `S` | Set — ayarlanır ve adım geçişleri arasında aktif kalır. |
| `R` | Reset — daha önce `S` ile ayarlanan bir eylemi temizler. |
| `L` | Sınırlı — en fazla verilen süre boyunca çalışır. |
| `D` | Gecikmeli — yalnızca verilen gecikmeden sonra başlar. |

Birden fazla eylem bloğu bir adıma dock edilebilir.

### Ayrılma ve birleşme

Bir **ayrılma** sırayı birden fazla yola dallandırır, bir **birleşme**
onları yeniden birleştirir. SFC'nin iki türü vardır:

* **Seçim (OR-ayrılması):** Hangi geçiş koşulunun önce TRUE olduğuna
  bağlı olarak yollardan **tam olarak biri** girilir. **Tek yatay çubuk**
  olarak çizilir.
* **Paralel (AND-ayrılması):** **Tüm** yollar aynı anda aktif olur ve
  bağımsız olarak çalışır. Yalnızca her biri birleşme noktasına
  ulaştığında sıra ilerler. **Çift yatay çubuk** olarak çizilir.

### Atlama

Bir atlama öğesi, hedef adımın adını taşıyan **aşağı yönlü bir oktur**.
Kontrolü mevcut yoldan adlandırılmış bir adıma aktarır — genellikle bir
sıranın sonunda "başa dön" için veya hata işleme için
("`Step_Error`'a atla") kullanılır.

## Uygulama

SFC, bir programın net bir **zamansal sıraya** sahip olduğu her durumda
uygundur:

* **Makine modları** — Init → Idle → Running → Cleanup → Idle.
* **Toplu süreçler** — Doldurma → Isıtma → Karıştırma → Boşaltma.
* **Güvenlik dizileri** — durdurma sıralarını tanımlı bir sırada
  gerçekleştirme ("önce ısıtıcı kapalı, sonra pompa kapalı, sonra ana
  konaktör").
* **Süreç mühendisliği** — gecikmeli ve koşullu reaksiyon adımları.

Aynı fonksiyonun bir ST uygulamasıyla karşılaştırıldığında, SFC sürümü
önemli ölçüde daha okunabilirdir — adım sırası ve dallanma koşulları
grafiksel olarak açıktır, oysa ST'de bir `CASE state OF` yapısı aynı
bilgiyi yalnızca dolaylı olarak iletir.

## İlgili konular

* [Function Block Diagram](../fbd/) — bir eylem **içindeki** veya bir
  geçiş koşulunun mantığı için.
* [Ladder Diagram](../ld/) — daha basit kilitleme devreleri için
  alternatif grafik dil.
* [Kütüphane](../library/) — zamanlayıcılar (`TON`, `TP`) geçiş
  koşullarının ortak parçalarıdır.
