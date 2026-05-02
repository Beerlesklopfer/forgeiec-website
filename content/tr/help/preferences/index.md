---
title: "Tercihler"
summary: "Merkezi düzenleyici yapılandırma diyalogu: Editor, Runtime, PLC, AI Assistant"
---

## Genel Bakış

**Preferences diyalogu**, tüm düzenleyici geneli ayarlar için tek giriş
noktasıdır — açık projenin parçası *olmayan* her şey, daha çok
düzenleyicinin kendisini, bir çalışma zamanına bağlantıyı ve yükleme
sonrası davranışı yapılandırır.

Diyaloğu **`Edit > Preferences...`** üzerinden açın (bazı temalar onu
`Tools > Preferences...` altına yerleştirir). Diyalog odaklıyken **F1**'e
basarak bu sayfayı doğrudan açabilirsiniz.

```
Preferences
+-- Editor          (font, tab width, line numbers)
+-- Runtime         (anvild host/port, Anvil debug, network scanner)
+-- PLC             (build mode, auto-start, persist, monitoring)
+-- AI Assistant    (LLM endpoint, tokens, temperature)
```

## Editor

ST kod düzenleyicisinde ve diğer her metin giriş alanında metnin nasıl
görüneceğini kontrol eder.

| Alan | Anlam |
|---|---|
| **Font**         | Yazı tipi ailesi. Monospace yazı tiplerine önceden filtrelenmiştir (önerilen: `JetBrains Mono`, `Cascadia Code`, `Consolas`). |
| **Font size**    | Punto cinsinden yazı tipi boyutu. Varsayılan `10`. |
| **Tab width**    | Tab başına boşluk sayısı. Varsayılan `4`. |
| **Show line numbers** | Kod düzenleyicinin oluğunda çalışan satır numaralarını gösterir. |

## Runtime

Bir **anvild** daemon'una bağlantı ve IPC tanılaması.

| Alan | Anlam |
|---|---|
| **Host**         | PLC hostname'i veya IP'si. Varsayılan `localhost`. |
| **Port**         | anvild gRPC portu. Varsayılan `50051`. |
| **User**         | Token kimlik doğrulaması için kullanıcı adı. |
| **Anvil Debug**  | IPC tanılama düzeyi (`Off`, `Errors only`, `Verbose`). anvild loguna ek istatistikler ekler — üretimde Iceoryx topic kaymasını izlemek için yararlıdır. |

Ayrıca: **Auto-Connect on start**, düzenleyici başlangıcında son
başarılı şekilde bağlanılan anvild'e otomatik olarak bağlanır — özel
bir mühendislik dizüstüsünde kullanışlıdır.

Aynı sekmedeki **Network Scanner** bloğu, LAN'ı Modbus TCP cihazları
(port 502) ve ForgeIEC çalışma zamanları (port 50051) için tarar ve
isabetleri bus yapılandırmasına ekler.

## PLC

PLC'ye **Upload**'tan sonra ne olacağını kontrol eder.

| Alan | Anlam |
|---|---|
| **Compile Mode** | `Development` (canlı izleme + zorlama etkin) veya `Production` (soyulmuş ikili, debug köprüleri yok — güvenlik sınırı). |
| **PLC autostart**| Başarılı bir yüklemeden sonra PLC çalışma zamanını otomatik olarak başlatır, onay diyaloğunu atlar. |
| **Persist enabled** | `VAR_PERSIST`/`RETAIN` değişkenlerinin `/var/lib/anvil/persistent.dat`'a periyodik kalıcılığını etkinleştirir. Değerler bir çalışma zamanı yeniden başlatmasından sonra korunur. |
| **Persist polling interval** | Otomatik kaydetme geçişleri arasındaki saniyeler (varsayılan `5 s`). |
| **Monitor history** | Osiloskop kaydedicideki değişken başına örnek sayısı (varsayılan `1000`). |
| **Monitor interval**| Canlı izleme için milisaniye cinsinden örnek aralığı (varsayılan `100 ms`). |

## Library

Düzenleyici kaynağı ile PLC tarafı kütüphane yolu arasında standart
kütüphane için senkronizasyon davranışı — tam sapma modeli için
[Library](../library/)'ye bakın. İki mod:

  - **Auto-Push kapalı** (varsayılan) — bağlantıda düzenleyici yalnızca
    sapma algılandığında Output panelinde bir ipucu loglar. Push
    `Tools > Sync Library` üzerinden manuel olarak gerçekleşir.
  - **Auto-Push açık** — algılanan her sapmada düzenleyici yerel
    kütüphane sürümünü otomatik olarak push eder. Tek programcılı bir
    kurulumda yararlıdır.

## AI Assistant

Yerel bir OpenAI uyumlu LLM sunucusuna karşı isteğe bağlı kod tamamlama
(LM Studio, Ollama, llama.cpp, vLLM).

| Alan | Anlam |
|---|---|
| **Enable AI Assistant** | Satır içi tamamlamayı açar/kapatır. |
| **API Endpoint**        | OpenAI uyumlu endpoint, örn. `http://localhost:1234/v1`. |
| **Max Tokens**          | İstek başına yanıt sınırı. Varsayılan `2048`. |
| **Temperature**         | `Precise (0.1)`, `Balanced (0.3)`, `Creative (0.7)`, `Wild (1.0)`. |

## UX durumu (otomatik kalıcı hale getirilir)

Aşağıdaki alanlar Preferences diyalogundan **geçmeden** arka planda
saklanır, böylece düzenleyici bıraktığınız tam durumda yeniden açılır:

  - Pencere geometrisi + pencere durumu (`windowGeometry`, `windowState`)
  - Splitter ve başlık konumları (`splitterState`, `headerState`)
  - Output panel yüksekliği (`outputPanelHeight`)
  - Son açılan proje (`lastProject`) ve yakın zamandaki dosyalar listesi
  - Oturum durumu: açık POU sekmeleri, etkin sekme, POU başına imleç
    ve kaydırma konumu

## Ayarların saklanması

Ayarlar Qt'nin `QSettings`'i aracılığıyla saklanır, platforma özgü:

| Platform | Yol |
|---|---|
| **Windows** | Registry: `HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

Bu dosyayı / registry anahtarını silmek tüm ayarları varsayılana
sıfırlar — başarısız bir yükseltmeden sonra yararlıdır.

## Planlanan eklentiler

Backlog (cluster R faz 3): Output paneli kendi önem dereceleri renklerini
(hata kırmızı, uyarı sarı, bilgi beyaz) ve yapılandırılabilir bir yazı
tipi boyutunu alacak. Her iki seçenek de daha sonra burada yeni bir
`Output` sekmesinde görünecek.

## İlgili konular

  - [Library](../library/) — düzenleyici ve çalışma zamanı arasındaki
    senkronizasyon davranışı.
  - [Bus configuration](../bus-config/) — burada *değil*, bus segmenti /
    cihazının kendisinde yaşayan proje kapsamlı ayarlar.
