---
title: "Périphériques de bus"
summary: "Configuration d'un périphérique au sein d'un segment de bus (esclave Modbus, esclave EtherCAT, ...)"
---

## Vue d'ensemble

Un **périphérique de bus** est un **périphérique unique au sein d'un
segment** — typiquement un esclave Modbus TCP (bloc d'E/S, variateur),
un esclave EtherCAT (axe servo, coupleur d'E/S), un esclave Profibus DP
ou un adaptateur EtherNet-IP. Pour chaque périphérique, le pont
responsable maintient une connexion logique, interroge les registres
configurés et publie les données via le groupe IPC Anvil vers le
runtime automate.

Un périphérique peut être **modulaire** : un coupleur de bus (slot 0)
porte 1..N modules d'E/S dans les slots 1..N. Les périphériques compacts
sans slots d'extension ont une liste `modules` vide — les variables
vivent alors directement sur le slot 0.

## Champs d'un périphérique

La définition de la struct se trouve dans
`editor/include/model/FBusSegmentConfig.h` (à côté du segment). Un
périphérique est persisté dans le projet `.forge` sous `<fi:device>` à
l'intérieur de `<fi:segment>` (voir [Configuration du bus](../)).

### Identité + adressage

| Champ | Type | Signification |
|---|---|---|
| `deviceId` | UUID | Clé primaire stable — auto-générée à la création. Survit au renommage du nom d'hôte et au changement d'IP, gardant tous les bindings de variables stables. |
| `hostname` | string | Étiquette visible par l'utilisateur (`"Maibeere"`, `"Stachelbeere"`). Compatible DHCP, mais explicitement **pas** la clé primaire. |
| `ipAddress` | string (IP) | Adresse IP (Modbus TCP / EtherNet-IP). Vide pour les périphériques sans IP (les esclaves EtherCAT s'identifient via leur position sur le bus). |
| `port` | int | Port TCP. Par défaut `502` (Modbus TCP). |
| `slaveId` | int | ID d'esclave Modbus (1..247). Habituellement `1` sur TCP. |
| `anvilGroup` | string | Groupe IPC Anvil pour le transport zero-copy entre le pont et le runtime automate. Convention : même nom que `hostname`. |
| `catalogRef` | string | Référence optionnelle vers une entrée de catalogue FDD (`"WAGO-750-352"`) décrivant le périphérique. |
| `description` | string | Description en texte libre (`"Bewaesserungsventil Sued"`). |

### Modules (slots)

| Champ | Type | Signification |
|---|---|---|
| `modules` | liste de `FBusModuleConfig` | Modules d'E/S du périphérique. Slot 0 = coupleur / périphérique compact, slots 1..N = modules d'extension. Par module : `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

### Surcharges par périphérique

Ces champs surchargent — uniquement pour **ce** périphérique — les
valeurs correspondantes du segment. `0` ou chaîne vide signifie *hériter
du segment*. Dans le panneau des propriétés ils se trouvent sous le bloc
*Advanced Overrides*, généralement replié.

| Champ | Type | Signification |
|---|---|---|
| `mac` | string `AA:BB:CC:DD:EE:FF` | Adresse MAC pour ARP statique / vérification d'identité. Protège contre l'usurpation d'IP sur les périphériques DHCP. |
| `endianness` | enum | Ordre des mots/octets pour les valeurs multi-registres : `"ABCD"` (big-endian, valeur par défaut IEC), `"DCBA"` (échange de mots), `"BADC"` (échange d'octets), `"CDAB"` (échange octets + mots). Vide = hériter du segment. |
| `timeoutOverrideMs` | int (ms) | Timeout par périphérique. `0` = utiliser le timeout du segment. |
| `retryCount` | int | Nombre de tentatives par requête. `0` = par défaut du segment. |
| `connectionMode` | enum | `"always"` (garde TCP ouvert entre les cycles) ou `"on_demand"` (reconnecte par transaction). Vide = par défaut du segment / pont. |
| `gatewayOverride` | string (IP) | Passerelle par périphérique lorsque le périphérique se trouve dans un sous-réseau différent de la carte réseau de bind. |

### Paramètres spécifiques au périphérique

La carte `settings` (clé/valeur) porte les valeurs qui n'ont de sens
que pour ce périphérique ou son type de périphérique — par ex. un seuil
d'un variateur ou un code de fonction préféré.

## Flux d'édition

| Action | Effet |
|---|---|
| **Clic simple** sur un nœud de périphérique | `FPropertiesPanel` affiche tous les champs comme éditeurs en ligne — bloc General (hostname, IP, port, slave ID, groupe Anvil), bloc Override (MAC, timeout, tentatives, endianness, mode de connexion, surcharge passerelle, description) et le tableau d'état. |
| **Double-clic** sur un nœud de périphérique | Ouvre la boîte de dialogue modale `FBusDeviceDialog` avec le même ensemble de champs. En mode édition, le bouton « Import from catalog » est verrouillé pour qu'un import FDD ultérieur ne puisse pas écraser silencieusement les bindings de variables d'E/S existants. |

## Variables d'état (lecture seule)

À l'exécution, chaque périphérique publie une structure d'état que le
démon envoie à travers le flux d'état gRPC. Ces valeurs sont affichées
dans le panneau des propriétés sous forme de **tableau en lecture
seule** et **ne sont pas éditables** depuis l'UI — c'est le pont qui
les écrit. Depuis le code ST, elles restent adressables comme chemins
qualifiés sous `anvil.<seg>.<dev>.Status.*` :

| Variable d'état | Type | Signification |
|---|---|---|
| `xOnline` | `BOOL` | Périphérique actuellement joignable (dernière requête répondue). |
| `eState` | `INT` | Énumération d'état : 0=offline, 1=connecting, 2=online, 3=error. |
| `wErrorCount` | `WORD` | Compteur de requêtes échouées depuis le démarrage du pont. |
| `sLastErrorMsg` | `STRING` | Dernier message d'erreur (timeout, exception Modbus, ...). |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## Exemple : coupleur de bus WAGO 750 avec deux slots

Un coupleur de bus Modbus TCP 750-352 avec un module 8-DI (750-430) sur
le slot 1 et un module 8-DO (750-530) sur le slot 2 :

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

Les 8 entrées apparaissent dans le pool d'adresses comme
`%IX0.0..%IX0.7` avec `deviceId="0e5d5537-..."`, `moduleSlot=1` et
`modbusAddress=0..7`. Les 8 sorties de même avec `moduleSlot=2`.

## Sujets liés

* [Segments de bus](../segments/) — le réseau dans lequel vit le
  périphérique.
* [Configuration du bus — vue d'ensemble du schéma](../) — persistance XML.
* [Format de fichier de projet](../../file-format/) — pool d'adresses et
  bindings variable-vers-périphérique.
