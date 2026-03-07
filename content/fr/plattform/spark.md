---
title: "Spark"
description: "Tunnel Zenoh -- pont reseau Edge-to-Cloud"
weight: 5
---

## Spark -- Tunnel Zenoh

Spark est le pont reseau Edge-to-Cloud de la plateforme ForgeIEC. L'etincelle
allume le feu -- Spark allume la connexion entre les automates sur site et les
services cloud.

---

## Edge-to-Cloud sans compromis

Les installations industrielles modernes necessitent une connexion fiable
entre les equipements de terrain et les services cloud -- pour la
tele-maintenance, l'analyse de donnees et la supervision a distance. Spark
fournit cette connexion via le protocole Zenoh.

### Pourquoi Zenoh ?

Zenoh est un protocole de communication concu pour les environnements
contraints et distribues. Contrairement aux VPN traditionnels ou aux
connexions MQTT, Zenoh offre :

- **Traversee NAT native** -- Pas de configuration de pare-feu complexe
- **Protocole pub/sub efficace** -- Faible consommation de bande passante
- **Routage adaptatif** -- Selection automatique du meilleur chemin reseau
- **Latence minimale** -- Concu pour les applications temps reel

---

## Cas d'utilisation

### Tele-maintenance

Connexion securisee aux automates distants pour le diagnostic, la mise a jour
de programmes et la lecture de variables -- sans deplacement sur site.

### Collecte de donnees cloud

Remontee des donnees de processus vers des plateformes cloud (AWS, Azure,
infrastructure privee) pour l'analyse, le machine learning et la
maintenance predictive.

### Supervision multi-sites

Surveillance centralisee de plusieurs installations depuis un point unique,
avec des donnees en temps reel et une latence minimale.

---

## Architecture

Spark fonctionne comme un daemon sur l'automate, connecte au runtime via
Anvil (Zero-Copy IPC). Les donnees sont transmises de maniere selective
vers les noeuds Zenoh distants.

```
Site A                           Cloud / Site central
+------------+                   +------------------+
| anvild     |                   | Zenoh Router     |
|   |        |                   |   |              |
|   +- Spark |----- Zenoh ---------|  +- Services   |
|   |  Anvil |   (chiffre)       |     Analytics    |
+------------+                   +------------------+
```

### Caracteristiques

- Chiffrement de bout en bout (TLS 1.3)
- Filtrage configurable des variables transmises
- Reconnexion automatique en cas de coupure reseau
- Compression des donnees pour les liaisons a faible debit
- Compatible avec les reseaux mobiles (4G/5G)

---

## Details techniques

- **Protocole** : Zenoh (zero overhead network protocol)
- **Transport** : TCP, UDP, WebSocket
- **Chiffrement** : TLS 1.3
- **Plateformes** : x86_64, ARM64, ARMv7 (Linux)
- **Integration** : Anvil IPC vers le runtime, Zenoh vers le cloud

---

<div style="text-align:center; padding: 2rem;">

**Spark -- L'etincelle qui connecte l'atelier au cloud.**

blacksmith@forgeiec.io

</div>
