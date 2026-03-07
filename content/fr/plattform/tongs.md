---
title: "Tongs"
description: "Bridges Fieldbus -- Modbus, EtherCAT, Profibus"
weight: 6
---

## Tongs -- Bridges Fieldbus

Les tenailles sont l'outil du forgeron pour saisir le metal brulant. **Tongs**
saisit les donnees des peripheriques de terrain et les transporte vers le
runtime de l'automate. Chaque protocole de bus de terrain dispose de sa propre
bridge, geree comme un processus independant.

---

## Protocoles supportes

### Modbus TCP

Communication Ethernet pour les peripheriques Modbus. Lecture et ecriture de
registres, bobines et entrees discretes. Scanner reseau integre pour la
detection automatique des peripheriques.

| Propriete | Valeur |
|-----------|--------|
| Transport | TCP/IP (Ethernet) |
| Bridge | `tongs-modbustcp` |
| Fonctions | FC1, FC2, FC3, FC4, FC5, FC6, FC15, FC16 |
| Statut | Disponible |

### Modbus RTU

Communication serie pour les peripheriques Modbus sur RS-485. Memes fonctions
que Modbus TCP, adaptees au transport serie.

| Propriete | Valeur |
|-----------|--------|
| Transport | Serie RS-485 |
| Bridge | `tongs-modbusrtu` |
| Statut | Disponible |

### EtherCAT

Bus de terrain Ethernet temps reel pour les variateurs, servomoteurs et
modules d'E/S haute performance.

| Propriete | Valeur |
|-----------|--------|
| Transport | Ethernet (temps reel) |
| Bridge | `tongs-ethercat` |
| Statut | En developpement |

### Profibus DP

Standard industriel eprouve pour la communication avec les peripheriques de
terrain dans les installations existantes.

| Propriete | Valeur |
|-----------|--------|
| Transport | RS-485 / Fibre optique |
| Bridge | `tongs-profibus` |
| Statut | En developpement |

---

## Architecture

Chaque bridge fonctionne comme un processus independant, gere par le daemon
`anvild`. La communication avec le runtime s'effectue via Anvil (Zero-Copy
IPC). Un crash d'une bridge n'affecte ni l'automate ni les autres bridges.

```
anvild
  |
  +-- tongs-modbustcp --segment mb1 --> Peripheriques Modbus TCP
  |
  +-- tongs-modbusrtu --segment mb2 --> Peripheriques Modbus RTU
  |
  +-- tongs-ethercat  --segment ec1 --> Peripheriques EtherCAT
  |
  +-- tongs-profibus  --segment pb1 --> Peripheriques Profibus
```

### Gestion des processus

- Demarrage automatique des bridges au lancement du runtime
- Surveillance continue -- redemarrage en cas de crash
- Un processus par segment de bus actif
- Journalisation independante par bridge

---

## Configuration

Les segments de bus sont configures dans `config.toml` sur le systeme cible.
Chaque segment definit le protocole, l'interface reseau et les peripheriques
connectes.

### Variables d'E/S

Chaque peripherique expose des variables d'entree et de sortie :

- **Direction "in"** -- Lecture depuis le peripherique (Subscribe)
- **Direction "out"** -- Ecriture vers le peripherique (Publish)
- Attribution automatique des adresses IEC (%I, %Q) sans conflits

---

<div style="text-align:center; padding: 2rem;">

**Tongs -- Les tenailles qui saisissent vos donnees de terrain.**

blacksmith@forgeiec.io

</div>
