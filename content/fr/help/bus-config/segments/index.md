---
title: "Segments de bus"
summary: "Configuration d'un segment de bus de terrain (un réseau physique sur une interface)"
---

## Vue d'ensemble

Un **segment de bus** décrit **un réseau physique sur une interface de
la cible automate** — typiquement un port Ethernet (`eth0`, `enp3s0`)
pour Modbus TCP / EtherCAT / EtherNet-IP, ou un port série
(`/dev/ttyUSB0`) pour Modbus RTU / Profibus DP. Pour chaque segment, le
démon `anvild` lance **exactement un processus pont** (`tongs-modbustcp`,
`tongs-ethercat`, ...) qui gère le trafic vers tous les périphériques de
ce segment.

Un projet peut contenir un nombre quelconque de segments — chacun avec
son propre protocole, sa propre interface et sa propre cadence
d'interrogation. Par exemple, un contrôleur d'axes EtherCAT rapide
(`eth1`, 1 ms) et un scrutateur de capteurs Modbus TCP lent (`eth0`,
100 ms) peuvent fonctionner côte à côte dans le même projet.

## Champs d'un segment

La définition de la struct se trouve dans
`editor/include/model/FBusSegmentConfig.h`. Un segment est persisté
dans le projet `.forge` sous `<fi:segment>` à l'intérieur de
`<fi:busConfig>` (voir [Configuration du bus](../)).

### Identité + protocole

| Champ | Type | Signification |
|---|---|---|
| `segmentId` | UUID | Clé primaire stable — auto-générée à la création, non modifiable. Survit au renommage, au changement de protocole et au changement d'IP. |
| `protocol` | enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Détermine quel démon pont est démarré. |
| `name` | string | Étiquette utilisateur (par ex. `"Fieldbus Hall 1"`). Forme libre, affichée dans l'arborescence et les journaux. |
| `enabled` | bool | Interrupteur on/off. `false` = le pont n'est pas démarré, les périphériques restent hors ligne. Par défaut : `true`. |

### Interface + routage

| Champ | Type | Signification |
|---|---|---|
| `interface` | string | Interface réseau (`eth0`, `enp3s0`, `/dev/ttyUSB0`). Transmise par le pont à l'API socket / série. |
| `bindAddress` | string (IP/CIDR) | IP source pour les connexions TCP sortantes, par ex. `192.168.24.100/24`. Vide = l'OS choisit la première IP de l'interface. |
| `gateway` | string (IP) | Passerelle par défaut pour les paquets quittant le sous-réseau local. Vide = pas de passerelle. |
| `pollIntervalMs` | int (ms) | Intervalle d'interrogation du pont. `0` = aussi vite que possible (busy loop / temps réel). Typique : `100` pour Modbus TCP, `0` pour EtherCAT. |

### Paramètres réseau (avancés)

Ces champs ont été ajoutés lors du sprint des paramètres réseau et
couvrent les cas où les valeurs par défaut de l'OS ne suffisent pas —
typiquement : nombreuses connexions TCP parallèles par esclave, sessions
TCP de longue durée à travers du NAT, ou plusieurs sous-réseaux sur une
seule carte réseau.

| Champ | Type | Signification |
|---|---|---|
| `subnetCidr` | string (CIDR) | Sous-réseau local du segment, par ex. `192.168.24.0/24`. Permet au pont de router correctement les surcharges de passerelle par périphérique lorsque la carte réseau de bind porte plusieurs réseaux. |
| `sourcePortRange` | string `"min-max"` | Plage de ports sources TCP pour les connexions sortantes, par ex. `30000-39999`. Vide = l'OS choisit dans la plage éphémère. Important lorsque de nombreuses connexions parallèles vers le même esclave sont nécessaires (une connexion par port source). |
| `keepAliveIdleSec` | int (s) | Secondes d'inactivité avant l'envoi de la première sonde keep-alive TCP. `0` = par défaut OS. |
| `keepAliveIntervalSec` | int (s) | Espacement entre les sondes keep-alive. `0` = par défaut OS. |
| `keepAliveCount` | int | Nombre de sondes échouées avant que la connexion soit déclarée morte. `0` = par défaut OS. |
| `maxConnections` | int | Borne supérieure du pool de connexions. `0` = illimité. Utile contre des esclaves avec une limite stricte de connexions. |
| `vlanId` | int (1..4094) | Tag VLAN 802.1Q pour les trames sortantes. `0` = non taggué. |

### Paramètres spécifiques au protocole

La carte `settings` (clé/valeur) contient toutes les valeurs qui n'ont
de sens que pour un protocole spécifique — par ex. pour Modbus TCP :
`port`, `timeout_ms` ; pour Modbus RTU : `serial_port`, `baud_rate`,
`parity`, `stop_bits` ; pour Profibus : `master_address`. `log_level`
et `log_file` sont également gardés indépendants du protocole dans cette
même carte.

## Flux d'édition

Dans le panneau de l'arborescence du bus, les deux chemins sont
équivalents — ils opèrent sur le même ensemble de champs et ont le même
effet sémantique :

| Action | Effet |
|---|---|
| **Clic simple** sur un nœud de segment | Le `FPropertiesPanel` (dock par défaut : côté droit) affiche tous les champs comme éditeurs en ligne — les modifications sont écrites dans le projet à `editingFinished` et marquent le projet modifié. |
| **Double-clic** sur un nœud de segment | Ouvre la boîte de dialogue modale `FSegmentDialog` avec le même ensemble de champs, regroupés en *General* / *Modbus TCP* / *Advanced Network* / *Logging*. OK valide, Annuler abandonne. |

## Exemple : segment Modbus TCP

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

Ce segment lance `tongs-modbustcp` sur `eth0` avec l'IP source
`192.168.24.100`, interroge tous les périphériques toutes les 100 ms et
accepte jusqu'à 2000 ms de temps de réponse par requête avant qu'une
erreur de timeout soit émise sur le flux d'état.

## Sujets liés

* [Configuration du bus — vue d'ensemble du schéma](../) — persistance
  XML et mécanisme PLCopen `<addData>`.
* [Périphériques de bus](../devices/) — périphériques au sein d'un segment.
* [Format de fichier de projet](../../file-format/) — la racine XML du
  `.forge`.
