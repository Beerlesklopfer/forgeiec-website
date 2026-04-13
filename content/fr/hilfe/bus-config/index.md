---
title: "Configuration Bus"
summary: "Schema XML PLCopen pour la configuration des bus de terrain industriels"
---

## Namespace

```
https://forgeiec.io/v2/bus-config
```

Ce schema decrit l'extension ForgeIEC du format XML PLCopen
pour le stockage de la configuration des bus de terrain dans les
fichiers de projet `.forge`. Il utilise le mecanisme `<addData>`
conforme au standard PLCopen TC6.

## Apercu

La configuration bus definit la topologie physique d'une installation :
les **segments** (reseaux de bus) contiennent des **devices** (appareils),
et chaque appareil est lie aux variables d'E/S du projet via un bus binding.

```
Projet .forge
  +-- Segments (reseaux de bus)
  |     +-- Devices (appareils)
  |           +-- Variables (via bus binding dans le pool d'adresses)
  +-- Pool d'adresses (FAddressPool)
        +-- Variable : DI_1, %IX0.0, busBinding -> Maibeere
        +-- Variable : DO_1, %QX0.0, busBinding -> Maibeere
```

## Structure XML

La configuration bus est stockee en tant que `<addData>` au niveau du projet :

```xml
<project>
  <!-- Contenu PLCopen standard -->
  <types>...</types>
  <instances>...</instances>

  <!-- Configuration bus ForgeIEC -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Bus de terrain Hall 1"
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

## Elements

### `fi:busConfig`

Element racine. Contient un ou plusieurs elements `fi:segment`.

| Attribut | Requis | Description |
|----------|--------|-------------|
| `xmlns:fi` | oui | Namespace : `https://forgeiec.io/v2` |

### `fi:segment`

Un segment de bus de terrain (reseau physique).

| Attribut | Requis | Type | Description |
|----------|--------|------|-------------|
| `id` | oui | UUID | Identifiant unique du segment |
| `protocol` | oui | String | Protocole : `modbustcp`, `modbusrtu`, `ethercat`, `profibus` |
| `name` | oui | String | Nom d'affichage (libre) |
| `enabled` | non | Bool | Segment actif (`true`) ou desactive (`false`). Defaut : `true` |
| `interface` | non | String | Interface reseau (ex. `eth0`, `/dev/ttyUSB0`) |
| `bindAddress` | non | String | IP/CIDR de l'interface (ex. `192.168.24.100/24`) |
| `gateway` | non | String | Adresse de la passerelle (vide = pas de passerelle) |
| `pollIntervalMs` | non | Int | Intervalle d'interrogation en millisecondes (`0` = aussi vite que possible) |

### `fi:device`

Un appareil au sein d'un segment.

| Attribut | Requis | Type | Description |
|----------|--------|------|-------------|
| `hostname` | oui | String | Nom de l'appareil (utilise comme identifiant) |
| `ipAddress` | non | String | Adresse IP (Modbus TCP) |
| `port` | non | Int | Port TCP (defaut : `502`) |
| `slaveId` | non | Int | Identifiant esclave Modbus |
| `anvilGroup` | non | String | Groupe Anvil IPC pour le transport zero-copie |

## Liaison Variable-Device

Les variables d'E/S ne sont **pas** listees dans l'element `fi:device`.
Chaque variable du pool d'adresses porte un attribut `busBinding`
pointant vers le `hostname` du device :

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

## Attribution des adresses IEC

L'adresse IEC d'une variable liee est derivee de la topologie physique :

```
Base du segment + Offset du device + Position du registre
```

| Plage d'adresses | Signification | Source |
|-------------------|---------------|--------|
| `%IX` / `%IW` / `%ID` | Entree physique | Bus binding |
| `%QX` / `%QW` / `%QD` | Sortie physique | Bus binding |
| `%MX` / `%MW` / `%MD` | Memento (pas d'E/S physique) | Allocateur de pool |

## Protocoles supportes

| Protocole | Valeur `protocol` | Medium | Daemon bridge |
|-----------|------------------|--------|---------------|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485 (serie) | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | Ethernet (temps reel) | `tongs-ethercat` |
| Profibus DP | `profibus` | Serie (bus de terrain) | `tongs-profibus` |

## Compatibilite

L'attribut `handleUnknown="discard"` garantit que les outils PLCopen
ne connaissant pas ForgeIEC peuvent ignorer la configuration bus sans
erreur. Inversement, ForgeIEC lit les blocs `<addData>` inconnus
d'autres fournisseurs et les preserve lors de la sauvegarde.

---

<div style="text-align:center; padding: 2rem;">

**Configuration Bus ForgeIEC — Hors ligne, conforme PLCopen, sans redondance.**

blacksmith@forgeiec.io

</div>
