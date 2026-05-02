---
title: "Panneau des propriétés"
summary: "Éditeur en ligne pour l'élément de bus sélectionné dans l'arborescence du projet"
---

## Vue d'ensemble

Le **panneau des propriétés** est la vue de détail à droite de la
fenêtre principale de l'éditeur. Il affiche **chaque champ de l'élément
actuellement sélectionné dans l'arborescence du projet** et rend ces
champs éditables en ligne — pas besoin d'ouvrir une boîte de dialogue
modale pour chaque édition.

```
Project tree                          Properties panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- click   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

Un **clic simple** sur un nœud d'arborescence rend immédiatement la
liste de champs correspondante — un **double-clic** ouvre en plus la
boîte de dialogue de configuration modale ([Configuration du
bus](../bus-config/)) avec exactement le même ensemble de champs.

Le panneau est encapsulé dans un `QScrollArea` et défile verticalement :
les périphériques avec extensions FDD plus le tableau d'état atteignent
facilement plus de 40 champs, et tous doivent rester accessibles même
lorsque le dock est étroit.

## Segment de bus

Lorsqu'un segment de bus est sélectionné, le panneau affiche :

| Champ | Signification |
|---|---|
| **Name** | Nom d'affichage dans l'arborescence du projet. |
| **Protocol** | `modbustcp`, `modbusrtu`, `ethercat`, `profibus`, `ethernetip`. |
| **Interface** | Interface réseau à laquelle le pont se lie (`eth0`, `eth1`, …). |
| **Bind Address** | Notation CIDR, par ex. `192.168.1.10/24`. Validée. |
| **Gateway** | Passerelle par défaut pour le processus pont. |
| **Poll Interval** | Période en `ms` à laquelle le pont interroge ses périphériques. |
| **Enabled** | Si le sous-processus du pont est actif. |

### Advanced Network (toutes optionnelles)

Reflète le même groupe dans `FSegmentDialog` et surcharge les valeurs
par défaut OS / pont :

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count** (heartbeat TCP)
  - **Max Connections** (`0` = illimité)
  - **VLAN ID** (`0` = non taggué)

### Spécifique au protocole

| Protocole | Champs |
|---|---|
| `modbustcp`  | `Port` (par défaut `502`), `Timeout` en `ms` (par défaut `2000`). |
| `modbusrtu`  | `Serial Port` (par ex. `/dev/ttyUSB0`), `Baud Rate`, `Parity` (`none`/`even`/`odd`). |
| `profibus`   | `Serial Port`, `Baud Rate` (jusqu'à 12 Mbit/s), `Master Address` (0..126). |

### Logging

  - **Log Level** — `off` / `error` / `warn` / `info` / `debug`.
  - **Log File** — par ex. `/var/log/forgeiec/segment.log`. Vide = stdout.

## Périphérique de bus

| Champ | Signification |
|---|---|
| **Hostname** | Nom DNS ou nom d'affichage. |
| **IP Address** | IPv4 du périphérique. |
| **Port** | Port Modbus sur l'esclave (par défaut `502`). |
| **Slave ID** | ID d'unité Modbus (0..247). |
| **Anvil Group** | Nom de groupe IPC Anvil — également le nom de l'`AnvilVarList` auto-généré. Le renommer renomme synchroniquement le tag GVL, l'AnvilVarList et chaque variable de pool avec `anvilGroup = oldGroup`. |

### Surcharges avancées (toutes optionnelles, vide = hériter du segment)

  - **MAC Address** — `AA:BB:CC:DD:EE:FF`. Validée.
  - **Endianness** — `ABCD` / `DCBA` / `BADC` / `CDAB`.
  - **Timeout** en `ms`. `0` = hériter du segment.
  - **Retry Count**. `0` = hériter du segment.
  - **Connection Mode** — `always connected` ou `on demand`.
  - **Gateway (override)** — uniquement quand le périphérique vit dans un sous-réseau différent.
  - **Description** — texte libre (par ex. `South irrigation valve`).

### Variables d'état (lecture seule)

Chaque périphérique expose automatiquement le modèle de défaut commun
— sept champs implicites publiés comme topic d'état en lecture seule
sur Anvil :

| Nom | Type IEC | Signification |
|---|---|---|
| `xOnline`              | `BOOL`         | TRUE quand `eState = Online` ou `Degraded`. |
| `eState`               | `eDeviceState` | État de défaut courant. |
| `wErrorCount`          | `UDINT`        | Total d'erreurs depuis le démarrage du pont. |
| `wConsecutiveFailures` | `UDINT`        | Échecs depuis le dernier `Online` (réinitialisé sur `Online`). |
| `wLastErrorCode`       | `UINT`         | `0` = aucune ; `1..99` communs ; `100+` spécifiques au protocole. |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8, complété par des zéros. |
| `tLastTransition`      | `ULINT`        | Heure Unix (ms) de la dernière transition d'état. |

Lorsque le périphérique est lié à une **FDD** (field device description)
via `catalogRef`, le tableau d'état liste en plus les extensions
définies par la FDD, marquées `FDD +<offset>` dans la colonne `Source`.

Dans le code ST, chaque variable d'état est accessible comme
`anvil.<seg>.<dev>.Status.*` :

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## Module de bus

Les modules de bus sont des tranches d'E/S à l'intérieur d'un
périphérique. Le panneau affiche :

### Métadonnées

  - **Module** (nom d'affichage ou `catalogRef`)
  - **Slot** (index de slot dans le périphérique)
  - **Catalog** (référence FDD, par ex. `Beckhoff.EL2008`)
  - **Base Addr** (décalage de base IEC)

### Tableau des variables d'E/S

Liste chaque variable de pool dont `busBinding.deviceId` et
`busBinding.moduleSlot` correspondent à ce module. Colonnes :

| Colonne | Contenu |
|---|---|
| **Name** | Nom du pool (éditable, par ex. `Motor_Run`). |
| **Type** | Type IEC (éditable, par ex. `BOOL`, `INT`). |
| **Address** | Adresse IEC (`%IX0.0`, lecture seule). |
| **Bus Addr** | Décalage de registre Modbus (lecture seule). |
| **Dir** | `in` ou `out` (lecture seule). |

Ordre de tri : entrées avant sorties, puis croissant par adresse de bus.

## Comportement d'édition

Chaque édition dans le panneau s'exécute directement contre le modèle :

  1. Édition sur le widget (`editingFinished` / `valueChanged` / `toggled`).
  2. Le champ du modèle est mis à jour (`seg->name = ...`).
  3. `project->markDirty()` lève le drapeau dirty.
  4. Le signal `busConfigEdited` est émis.
  5. La fenêtre principale rafraîchit le label de l'arborescence du
     projet si nécessaire.

Il n'y a **pas** d'`Apply` explicite et **pas** de `Cancel` — les
modifications prennent effet immédiatement. `Ctrl+Z` (undo) sur
l'arborescence du projet annule la dernière modification.

## Sujets liés

  - [Configuration du bus](../bus-config/) — boîtes de dialogue modales
    avec le même ensemble de champs, pour les utilisateurs avancés à
    fort volume d'édition.
  - [Panneau des variables](../variables/) — le pool qui alimente le
    tableau `IO variables`.
