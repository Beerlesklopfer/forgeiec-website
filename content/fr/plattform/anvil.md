---
title: "Anvil"
description: "Runtime automate en temps reel avec IPC Zero-Copy"
weight: 2
---

## Anvil -- Le runtime au coeur de la forge

Dans chaque forge, l'enclume est la piece maitresse -- la ou le metal est
forme, trempe et affine. **Anvil** est la couche intermediaire entre le
runtime de l'automate et les bridges de protocole. C'est ici que vos donnees
de processus sont forgees : recues, transformees et distribuees aux bons
destinataires.

Anvil utilise une couche de transport proprietaire en memoire partagee
Zero-Copy pour la communication inter-processus. Pas de serialisation,
pas de copies, pas de compromis.

---

## Architecture

```
+--------------+         +------------+         +------------------+
|              |         |            |         |                  |
| Programme    |<------->|  anvild    |<------->|  Modbus Bridge   |---> Peripheriques
|  automate    |  gRPC   |  (Daemon)  |  Anvil  |  EtherCAT Bridge |---> Variateurs
|  (Code IEC)  |         |            |         |  Profibus Bridge |---> Capteurs
+--------------+         +------------+         |  OPC-UA Bridge   |---> SCADA
                                                +------------------+

                         <--- Anvil --->
                         Zero-Copy IPC
                         Memoire partagee
```

L'echange de donnees entre `anvild` et les bridges de protocole s'effectue
via **Anvil** -- un canal IPC haute performance base sur la memoire partagee
Zero-Copy. Chaque segment recoit son propre canal de communication.

---

## Pourquoi Anvil ?

### Latence en microsecondes

Les mecanismes IPC conventionnels (pipes, sockets, files de messages) copient
les donnees entre les processus. Anvil elimine chaque copie. Les donnees
resident en memoire partagee -- le recepteur lit directement.

| Methode | Latence typique | Copies |
|---------|----------------|--------|
| TCP Socket | 50-200 us | 2-4 |
| Unix Socket | 10-50 us | 2 |
| **Anvil** | **< 1 us** | **0** |

### Qualite industrielle

- Comportement deterministe -- aucune allocation memoire dynamique dans le chemin critique
- Algorithmes sans verrou -- pas de blocage, pas de deadlock
- Modele Publish/Subscribe -- couplage lache entre producteur et consommateur
- Gestion automatique du cycle de vie -- les bridges sont surveillees et redemarrees en cas de crash

### PUBLISH/SUBSCRIBE dans le programme IEC

Anvil s'integre de maniere transparente dans la programmation IEC 61131-3 :

```iec
VAR_GLOBAL PUBLISH 'Moteurs'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Vitesse  AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Capteurs'
    Temperature AT %IW0   : INT;
    Pression    AT %IW2   : INT;
END_VAR
```

Les mots-cles PUBLISH/SUBSCRIBE sont une extension ForgeIEC du standard
IEC 61131-3. Le compilateur genere automatiquement les liaisons Anvil.

---

## Protocoles supportes

| Protocole | Bridge | Statut |
|-----------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | Disponible |
| **Modbus RTU** | `tongs-modbusrtu` | Disponible |
| **EtherCAT** | `tongs-ethercat` | En developpement |
| **Profibus DP** | `tongs-profibus` | En developpement |
| **OPC-UA** | `tongs-opcua` | Planifie |

Chaque bridge fonctionne comme un processus independant. `anvild` demarre,
surveille et redemarre les bridges automatiquement. Un crash d'une bridge
n'affecte ni l'automate ni les autres bridges.

---

## Details techniques

- **Framework IPC** : Anvil (memoire partagee Zero-Copy proprietaire)
- **Architecture** : Un canal publisher/subscriber par segment de bus
- **Format des donnees** : Variables IEC brutes -- aucune serialisation, aucun overhead
- **Plateformes** : x86_64, ARM64, ARMv7 (Linux)
- **Modele de processus** : Un processus bridge par segment actif

---

<div style="text-align:center; padding: 2rem;">

**Anvil -- La ou les donnees sont forgees en commandes de controle.**

blacksmith@forgeiec.io

</div>
