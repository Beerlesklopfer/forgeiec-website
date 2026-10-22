---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# Enduestri icin doevuelmues.

**Enduestri kalitesinde IEC 61131-3 gelistirme ortami. Acik kaynak.**

[Iletisim](mailto:blacksmith@forgeiec.io)

</div>

---

## Ne insa ediyoruz

ForgeIEC, endustriyel otomasyon icin eksiksiz bir IEC 61131-3 gelistirme
ortamidir — bes IEC dili, endustriyel bus sistemleri, gercek zamanli
hata ayiklama.

Yerlesik ticari sistemlerle esit kosullarda rekabet etme hedefiyle
gelistirilmektedir. Her ozellik, yayin oncesi belgelenmis testlerle
dogrulanir.

---

## Neden acik kaynak

Endustriyel otomasyon kritik bir teknolojidir. Ancak profesyonel araclara
erisim, lisans maliyetleri ve tescilli sistemler tarafindan kisitlanmaktadir.
ForgeIEC, otomasyonun degerini herkes icin erisilebilir kilar — satici
bagimliligi yok, lisans uecreti yok.

Acik kaynak projesi olarak ForgeIEC topluluga aittir.

---

## Başlarken

```bash
# İmza anahtarını ekleyin (bir kez)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Depo kaynağını ekleyin
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# Editör + çalışma zamanını kurun
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

Debian 13 (trixie) için gösterilmiştir. Debian 12 (bookworm) veya Ubuntu 24.04 (noble) için `trixie` geçen iki yeri değiştirin. Tüm dağıtımlar, RPM ve diğer paketler: [İndir](/download/).

---

<div style="text-align:center; padding: 2rem;">

**Enduestri kalitesinde bir sueruem hazir oldugunda
ayrintili bilgi yayinlayacagiz.**

blacksmith@forgeiec.io

</div>
