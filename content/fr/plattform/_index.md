---
title: "Plateforme"
description: "La plateforme ForgeIEC -- tous les composants pour l'automatisation industrielle"
weight: 10
---

## La plateforme ForgeIEC

ForgeIEC est une plateforme d'automatisation industrielle complete -- de
l'environnement de developpement jusqu'au systeme de supervision. Chaque
composant porte le nom d'un outil de forgeron, car ForgeIEC est forge pour
l'industrie.

---

### Forge Studio

**Environnement de developpement IEC 61131-3**

L'IDE professionnel pour la programmation d'automates. Les cinq langages IEC,
edition graphique et textuelle, compilation locale, deploiement a distance.
Construit avec C++17 et Qt6.

[En savoir plus](forge-studio/)

---

### Anvil

**Runtime automate en temps reel**

Le daemon de runtime qui execute les programmes IEC sur le systeme cible.
Communication Zero-Copy entre le runtime et les bridges de protocole via
la technologie Anvil de memoire partagee.

[En savoir plus](anvil/)

---

### Bellows

**Passerelle OPC UA** -- En cours de developpement

Communication machine-a-machine conforme au standard OPC UA. Integration
transparente des systemes d'automatisation dans l'infrastructure IT existante.

[En savoir plus](bellows/)

---

### Hearth

**SCADA/IHM** -- En cours de developpement

Visualisation de processus et interface homme-machine pour la supervision
industrielle. Tableaux de bord en temps reel, historique des donnees,
gestion des alarmes.

[En savoir plus](hearth/)

---

### Spark

**Tunnel Zenoh**

Pont reseau Edge-to-Cloud base sur le protocole Zenoh. Connexion securisee
entre les automates sur site et les services cloud, sans VPN, sans
configuration complexe.

[En savoir plus](spark/)

---

### Tongs

**Bridges Fieldbus**

Les ponts de protocole pour Modbus TCP/RTU, EtherCAT et Profibus DP. Chaque
bridge fonctionne comme un processus independant, supervise et redemarre
automatiquement par le runtime.

[En savoir plus](tongs/)

---

### Ledger

**Gestion des ordres de fabrication** -- En cours de developpement

Integration MES pour la gestion des ordres de fabrication, le suivi de
production et la tracabilite. Pont entre l'automatisation et la planification
de la production.

[En savoir plus](ledger/)

---

<div style="text-align:center; padding: 2rem;">

**Base sur OpenPLC** — ForgeIEC est base sur le projet
[OpenPLC](https://autonomylogic.com/) et est entierement compatible avec
son architecture de fichiers. Les projets OpenPLC existants peuvent etre
ouverts et developpes directement.

**Tous les composants sont Open Source. Pas de frais de licence. Pas de dependance fournisseur.**

blacksmith@forgeiec.io

</div>
