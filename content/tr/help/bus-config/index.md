---
title: "Bus Yapilandirmasi"
summary: "Endustriyel saha bus yapilandirmasi icin PLCopen XML semasi"
---

## Ad Alani

```
https://forgeiec.io/v2/bus-config
```

Bu sema, `.forge` proje dosyalarinda saha bus yapilandirmasini
saklamak icin PLCopen XML formatinin ForgeIEC uzantisini tanimlar.
PLCopen TC6 tarafindan tanimlanan standart uyumlu `<addData>`
mekanizmasini kullanir.

## Genel Bakis

Bus yapilandirmasi bir tesisin fiziksel topolojisini tanimlar:
**Segmentler** (saha bus aglari) **cihazlari** icerir ve her
cihaz, bus baglama yoluyla projenin G/C degiskenlerine baglidir.

```
.forge Proje
  +-- Segmentler (saha bus aglari)
  |     +-- Cihazlar
  |           +-- Degiskenler (adres havuzundaki bus baglama ile)
  +-- Adres Havuzu (FAddressPool)
        +-- Degisken: DI_1, %IX0.0, busBinding -> Maibeere
        +-- Degisken: DO_1, %QX0.0, busBinding -> Maibeere
```

## XML Yapisi

Bus yapilandirmasi proje seviyesinde `<addData>` olarak saklanir:

```xml
<project>
  <!-- Standart PLCopen icerigi -->
  <types>...</types>
  <instances>...</instances>

  <!-- ForgeIEC bus yapilandirmasi -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Saha Bus Salon 1"
                    enabled="true"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    gateway=""
                    pollIntervalMs="0">

          <fi:device hostname="Maibeere"
                     ipAddress="192.168.24.25"
                     port="502"
                     slaveId="1"
                     anvilGroup="Maibeere"/>

          <fi:device hostname="Stachelbeere"
                     ipAddress="192.168.24.26"
                     port="502"
                     slaveId="1"
                     anvilGroup="Stachelbeere"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

## Elemanlar

### `fi:busConfig`

Kok eleman. Bir veya daha fazla `fi:segment` elemani icerir.

| Ozellik | Gerekli | Aciklama |
|---------|---------|----------|
| `xmlns:fi` | evet | Ad alani: `https://forgeiec.io/v2` |

### `fi:segment`

Bir saha bus segmenti (fiziksel ag).

| Ozellik | Gerekli | Tip | Aciklama |
|---------|---------|-----|----------|
| `id` | evet | UUID | Benzersiz segment tanimlayicisi |
| `protocol` | evet | String | Protokol: `modbustcp`, `modbusrtu`, `ethercat`, `profibus` |
| `name` | evet | String | Goruntuleme adi (serbest) |
| `enabled` | hayir | Bool | Segment etkin (`true`) veya devre disi (`false`). Varsayilan: `true` |
| `interface` | hayir | String | Ag arayuzu (orn. `eth0`, `/dev/ttyUSB0`) |
| `bindAddress` | hayir | String | Arayuz icin IP/CIDR (orn. `192.168.24.100/24`) |
| `gateway` | hayir | String | Gecit adresi (bos = gecit yok) |
| `pollIntervalMs` | hayir | Int | Sorgulama araligi (ms) (`0` = mumkun oldugunca hizli) |

### `fi:device`

Bir segment icindeki cihaz.

| Ozellik | Gerekli | Tip | Aciklama |
|---------|---------|-----|----------|
| `hostname` | evet | String | Cihaz adi (cihaz kimlik olarak kullanilir) |
| `ipAddress` | hayir | String | IP adresi (Modbus TCP) |
| `port` | hayir | Int | TCP portu (varsayilan: `502`) |
| `slaveId` | hayir | Int | Modbus slave kimlik |
| `anvilGroup` | hayir | String | Sifir kopya tasima icin Anvil IPC grubu |

## Degisken-Cihaz Baglama

G/C degiskenleri `fi:device` elemani icinde **listelenmez**.
Bunun yerine, adres havuzundaki her degisken, cihazin `hostname`
degerine isaret eden bir `busBinding` ozelligine sahiptir:

```
FLocatedVariable
  name: "DI_1"
  address: "%IX0.0"
  anvilGroup: "Maibeere"
  busBinding:
    deviceId: "Maibeere"
    modbusAddress: 0
    count: 1
```

## IEC Adres Atamasi

Bagli bir degiskenin IEC adresi fiziksel topolojiden turetilir:

```
Segment Tabani + Cihaz Ofseti + Register Pozisyonu
```

| Adres Araligi | Anlami | Kaynak |
|---------------|--------|--------|
| `%IX` / `%IW` / `%ID` | Fiziksel giris | Bus baglama |
| `%QX` / `%QW` / `%QD` | Fiziksel cikis | Bus baglama |
| `%MX` / `%MW` / `%MD` | Isaretci (fiziksel G/C yok) | Havuz ayiricisi |

## Desteklenen Protokoller

| Protokol | `protocol` Degeri | Ortam | Kopru Daemonu |
|----------|------------------|-------|---------------|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485 (seri) | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | Ethernet (gercek zamanli) | `tongs-ethercat` |
| Profibus DP | `profibus` | Seri (saha bus) | `tongs-profibus` |

## Uyumluluk

`handleUnknown="discard"` ozelligi, ForgeIEC'yi tanimayan PLCopen
uyumlu araclarin bus yapilandirmasini hatasiz guvenlice yok
sayabilmesini saglar. Tersine, ForgeIEC diger ureticilerin bilinmeyen
`<addData>` bloklarini okur ve kaydetme sirasinda korur.

---

<div style="text-align:center; padding: 2rem;">

**ForgeIEC Bus Yapilandirmasi — Cevrimdisi, PLCopen uyumlu, fazlaliktan arinmis.**

blacksmith@forgeiec.io

</div>
