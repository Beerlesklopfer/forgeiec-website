---
title: "İndir"
summary: "Tüm ForgeIEC bileşenleri — APT ve RPM depoları, doğrudan indirmeler, kaynak kodu"
---

## ForgeIEC bileşenlerine genel bakış

ForgeIEC birkaç bileşenden oluşur. Hangilerine ihtiyacınız olduğu
rolünüze bağlıdır:

| Rol | Bileşen | Nereye kurulur |
|---|---|---|
| **PLC programcısı / kullanıcı** | `forgeiec-studio` | İş istasyonu |
| **Devreye alma mühendisi** | `forgeiec-anvil-server` (`anvild` içerir) | Hedef PLC |
| **HMI / OPC-UA köprüsü** | `forgeiec-bellows-server` (`bellowsd` içerir) | Hedef PLC veya ayrı bir sunucu |
| **Modbus TCP** | `forgeiec-anvil-server` içinde | Hedef PLC |
| **Profibus / EtherCAT / EthernetIP** | aynı şekilde `forgeiec-anvil-server` içinde | Hedef PLC |
| **Operatör paneli** | `forgeiec-screen-wayland` veya `-xorg` | Panel donanımı |

---

## Paket deposundan kurulum

ForgeIEC, `apt.forgeiec.io` adresinde imzalı bir Debian deposu ve
`rpm.forgeiec.io` adresinde imzalı bir RPM deposu olarak sunulur.
Kurulum her iş istasyonu veya hedef PLC için bir kez yapılır —
dağıtımınızı seçin:

{{< distro-install >}}

Ardından bileşenleri tek tek kurun:

```bash
# İş istasyonu
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # Cihaz tanımları (önerilir)

# Hedef PLC
sudo apt install forgeiec-anvil-server    # PLC çalışma zamanı (anvild + tüm tongs-*)
sudo apt install forgeiec-bellows-server  # HMI geçidi (bellowsd)

# Operatör paneli
sudo apt install forgeiec-screen-wayland  # Wayland üzerinde kiosk
sudo apt install forgeiec-screen-xorg     # X11 üzerinde kiosk
```

RPM sistemlerinde komutlar, paket adları aynı kalmak üzere
`sudo dnf install …` şeklindedir.

Bus köprüleri (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) ayrı paketler **değildir** — `forgeiec-anvil-server`
içinde bulunurlar ve `anvild` tarafından başlatılırlar.

Güncellemeler standart `apt update && apt upgrade` döngüsünü izler —
elle `.deb` dosyası gerekmez.

---

## Desteklenen platformlar

### Debian / Ubuntu (`apt.forgeiec.io`)

| Paket | Mimariler | Sürümler (suite) |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | mimariden bağımsız | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

Suite eşleşmesi: `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Paket | Mimari | Dağıtımlar |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

RPM dağıtımı yenidir ve şu anda yalnızca operatör panelini kapsar.
ForgeIEC Studio ve çalışma zamanı, RPM paketleri kararlı hale gelince
eklenecektir.

**İki farklı imza anahtarı** vardır: apt için `forgeiec.gpg` (ed25519),
rpm için `forgeiec-rpm.asc` (RSA-4096). Bu fark kozmetik değildir —
RHEL 9, dahili PGP ayrıştırıcısı ed25519 doğrulayamayan `rpm` 4.16 ile
gelir.

RPM tarafında arm64 bilinçli olarak yoktur: CI'daki çapraz derleme yolu,
Enterprise Linux'ta bulunmayan Debian paketlerine dayanır.

ForgeIEC Studio'nun **Windows sürümü**: hazırlanıyor. O zamana kadar
Studio, Linux'ta yerel olarak veya Windows iş istasyonlarında WSL2
üzerinden çalışır.

---

## Doğrudan indirmeler (sürüm arşivleri)

Paket deposunu kullanamıyor ya da kullanmak istemiyorsanız — örneğin
ağdan yalıtılmış (air gap) iş istasyonları için — tek tek sürümleri
Forgejo'dan alabilirsiniz. **Depolar herkese açık olarak gezilemez**:
SSH açık anahtarınızı blacksmith@forgeiec.io adresine gönderin, biz
de etkinleştirelim. Ardından şu depolar size açılır:

- **ForgeIEC Studio kaynak kodu**: `ForgeIEC/forgeiec-studio`
- **anvild + köprüler**: `ForgeIEC/anvil`
- **bellowsd**: `ForgeIEC/bellows`
- **Web sitesi kaynak kodu**: `ForgeIEC/forgeiec-website`

Her sürümde imzalı `.deb` paketleri ve kaynak arşivleri Forgejo'daki
sürüm etiketine eklenir.

---

## Kaynaktan derleme

```bash
# Depoyu (alt modüllerle) klonlayın — yalnızca SSH ile, SSH açık
# anahtarınız etkinleştirildikten sonra
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# Studio + tüm daemon'ları derleyin
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# Yerel sisteme dağıtın
./deploy.sh all
```

Ön koşullar:

- Debian 12/13 veya Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+ (rustup ile)

---

## Demo projeleri

ForgeIEC Studio ile birlikte gelen örnek projeler:

| Proje | Amaç |
|---|---|
| `knight_rider.forge` | Bellows LED'leri için klasik kayan ışık testi |
| yenileri gelecek | … |

Studio'da `File → Open Example` altında bulunur.

---

## Sonraki adımlar

- [ForgeIEC Studio ile ilk adımlar](/help/)
- [Yapay zekâ asistanını kurma](/en/help/ai/) (İngilizce)
- [Bus yapılandırması](/help/bus-config/)
- [Haberler + sürüm notları](/en/news/) (İngilizce)
