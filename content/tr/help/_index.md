---
title: "Yardim"
summary: "ForgeIEC dokuemantasyonu ve kaynaklari"
---

## Yardim ve Kaynaklar

ForgeIEC yardim boeluemune hosgeldiniz. Burada projemizin temelleri ve
felsefemiz hakkinda bilgi bulabilirsiniz.

---

## Konular

### [Bus Yapilandirmasi](/help/bus-config/)

`.forge` projelerinde endustriyel saha bus yapilandirmasi icin PLCopen XML
semasi. Segmentler, cihazlar, degisken baglama ve IEC adres atamasi.

### [Test Kapsami](/help/tests/)

117 otomatik test, tam IEC 61131-3 dil ozellik setini, tum 132 standart
kutuphane blogunu ve coklu gorev is parcacigi sistemini dogrular.

### [Acik Kaynak Felsefesi](/help/open-source/)

Acik kaynagin arkasindaki fikir yazilimin cok oetesine gider — bilgiyi
oezgueruestiren ve inovasyonu demokratiklestiren bir harekettir.

---

## Baslarken

ForgeIEC iki bilesenden olusur:

1. **ForgeIEC Editoer** (`forgeiec`) — Is istasyonunuzdaki gelistirme ortami
2. **ForgeIEC Daemon** (`anvild`) — Hedef PLC uzerindeki calisma zamani sistemi

### ForgeIEC APT Deposundan Kurulum

ForgeIEC, `apt.forgeiec.io` adresinde imzali bir Debian deposu olarak
sunulmaktadir. Kurulum her is istasyonu veya hedef PLC'de bir kez
yapilir:

```bash
# Imza anahtarini iceri aktar
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Depo kaynagini ekle
# (Debian 12 "bookworm" veya Debian 13 "trixie" — sisteminize uygun olani)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Ardindan standart paket yoeneticisi ile herhangi bir ForgeIEC paketini
kurabilirsiniz:

```bash
# Editoer (is istasyonu)
sudo apt install forgeiec

# Daemon (hedef PLC)
sudo apt install anvild
```

Guecellemeler normal `apt update && apt upgrade` yaşam doengusuenue
takip eder — manuel `.deb` dosyalarina gerek yoktur.

### Desteklenen Platformlar

| Bilesen  | Mimariler     | Debian Sueruemleri |
|----------|---------------|--------------------|
| Editoer  | amd64, arm64  | bookworm, trixie   |
| Daemon   | amd64, arm64  | bookworm, trixie   |
| Bridges  | amd64, arm64  | bookworm, trixie   |
| Hearth   | amd64, arm64  | bookworm, trixie   |

### Iletisim

Sorulariniz icin: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**Dokuemantasyon projeyle birlikte bueyer.**

blacksmith@forgeiec.io

</div>
