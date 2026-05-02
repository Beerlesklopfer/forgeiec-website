---
title: "Function Block Diagram Düzenleyici (FBD)"
summary: "Fonksiyonların, fonksiyon bloklarının ve değişkenlerin grafik bağlantısı"
---

## Genel Bakış

Function Block Diagram (FBD), ForgeIEC Studio tarafından desteklenen
üç grafik IEC 61131-3 dilinden biridir. Bir FBD programı, **fonksiyon
ve fonksiyon bloğu çağrılarının** birbirine ve giriş/çıkış değişkenlerine
**açık tel bağlantıları** aracılığıyla bağlanmasından oluşur. Ladder
Diagram'ın aksine, FBD'nin **güç rayları yoktur**: her bağlantı, bir
çıkış pinini bir veya daha fazla giriş pinine taşıyan tek bir teldir.

## Düzenleyici düzeni

FBD düzenleyicisi üç parçalı bir widget'tır:

```
+---------------------------------------------+
| Toolbar (Select | Wire | Block | Var | ...) |
+--------------------------------+------------+
|                                |            |
|       QGraphicsView            |  Variable  |
|       Grid + Zoom + Pan        |  table     |
|                                |  (right)   |
|                                |            |
+--------------------------------+------------+
```

* **Üstteki araç çubuğu:** Araç değiştirme (Select, Wire, Place Block,
  Place In-/Out-Variable, Comment, Zoom).
* **QGraphicsView:** Arka plan ızgarası (10 px ince, 50 px kalın) ve
  orta tıklama kaydırma ile çizim yüzeyi. Fare tekerleği imleç
  etrafında yakınlaştırma yapar.
* **Sağdaki değişken tablosu:** Dock edilebilir, POU'nun yerel
  değişkenlerini gösterir. Tablodan sürükle-bırak, düzenleyicide bir
  giriş/çıkış değişkeni öğesi oluşturur.

## Araçlar

| Araç | Etki |
|---|---|
| **Select** | Öğeleri seç, taşı, sil. |
| **Wire** | Bir çıkış portuna tıklayın, ardından bir giriş portuna tıklayın — bağlantı oluşturulur. |
| **Place Block** | Kütüphaneden bir fonksiyon veya fonksiyon bloğu bırakın. Pin listesi (girişler solda, çıkışlar sağda) kütüphane tanımından alınır. |
| **InVar / OutVar** | Bir giriş veya çıkış değişkeni öğesi yerleştirin. Ad bir diyalog aracılığıyla girilir ve GVL-, Anvil- veya Bellows-nitelikli bir değişken olabilir. |
| **Comment** | Anlamsal etkisi olmayan serbest metin notu. |

## Bloklar ve pinler

Bir **blok öğesi**, bir fonksiyona (`ADD`, `SEL`, ...) veya bir
fonksiyon bloğuna (`TON`, `CTU`, ...) yapılan bir çağrıyı temsil eder.
Öğe, başlıkta tip adını, altında örnek adını (yalnızca FB) ve
yanlarda portları gösterir:

```
        +---- TON -----+
        | tonA         |
   IN --| IN          Q|-- timeUp
   PT --| PT         ET|-- elapsed
        +--------------+
```

Girişler **her zaman solda**, çıkışlar **her zaman sağdadır**. Negatif
pinler portta küçük bir daire ile işaretlenir.

## Kütüphane sürükleme

Kütüphane panelinden, herhangi bir standart veya kullanıcı bloğu
**doğrudan düzenleyiciye sürüklenip bırakılabilir**. Bırakıldığında pin
listesi kütüphane tanımından alınır; fonksiyon blokları için düzenleyici
yerel değişken bölümünde otomatik olarak bir `VAR` örnek girişi oluşturur.

## ST'ye round-trip

Derleme zamanında ForgeIEC derleyici, FBD gövdesini Structured Text'e
çevirir. Blokların veri akışına göre topolojik sıralaması yürütme
sırasını belirler. Bu nedenle: **herhangi bir FBD gövdesi anlamsal
olarak bir ST gövdesine eşdeğerdir** ve dil seçimi tamamen okunabilirlik
meselesidir.

## Örnek — `TON` ile açma gecikmeli zamanlayıcı

Bir `TON` (açma gecikmeli zamanlayıcı), bir giriş sinyalini
yapılandırılabilir bir süre kadar geciktirir. FBD'de şunu yaparsınız:

  * `TON` örneğinin `IN` pinine bir **giriş değişkenini** `start` bağlayın,
  * `T#5s` değerine sahip bir **giriş değişkenini** `PT` pinine bağlayın,
  * `Q` çıkışını bir **çıkış değişkenine** `lampe`'ye bağlayın.

ST'de bu şu şekilde görünür:

```text
PROGRAM PLC_PRG
VAR
    start  AT %IX0.0 : BOOL;
    lampe  AT %QX0.0 : BOOL;
    tmr    : TON;
END_VAR

tmr(IN := start, PT := T#5s);
lampe := tmr.Q;
END_PROGRAM
```

Bu tam olarak derleyicinin FBD diyagramından ürettiği şekildir —
değişken örneği `tmr` `Block` kutusudur ve iki tel iki `:=` atamasıdır.

## İlgili konular

* [Kütüphane](../library/) — blok seçicinin sunduğu bloklar.
* [Variables Panel](../variables/) — değişken tanımı ve adres havuzu.
* [Ladder Diagram](../ld/) — akım yolu odaklı kardeş dil.
