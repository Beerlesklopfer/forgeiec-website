---
title: "Bellows"
description: "Passerelle OPC UA pour la communication machine-a-machine"
weight: 3
---

## Bellows -- Passerelle OPC UA

**En cours de developpement**

Bellows est la passerelle OPC UA de la plateforme ForgeIEC. Le soufflet de
forge alimente le feu -- Bellows alimente la communication entre les systemes
d'automatisation et l'infrastructure IT.

---

## Communication machine-a-machine

OPC UA (Open Platform Communications Unified Architecture) est le standard
de communication pour l'industrie 4.0. Bellows fournit un serveur OPC UA
complet qui expose les variables de l'automate aux systemes de niveau
superieur.

### Cas d'utilisation prevus

- **Integration SCADA** -- Connexion des automates aux systemes de supervision existants
- **Echange de donnees M2M** -- Communication directe entre automates et systemes tiers
- **Passerelle IT/OT** -- Pont entre les reseaux d'automatisation et l'infrastructure informatique
- **Historisation** -- Mise a disposition des donnees de processus pour l'archivage

---

## Architecture prevue

Bellows fonctionnera comme un processus independant, gere par le daemon
`anvild`. Les donnees de processus sont recues via Anvil (Zero-Copy IPC)
et exposees via le protocole OPC UA.

```
Automate  --->  anvild  --->  Bellows (OPC UA Server)  --->  Clients OPC UA
                 Anvil IPC                                    SCADA, MES, Cloud
```

### Fonctionnalites planifiees

- Serveur OPC UA conforme a la specification
- Exposition automatique des variables IEC
- Modele d'information configurable
- Chiffrement et authentification
- Decouverte automatique des services
- Historique des donnees integre

---

## Securite

- Chiffrement TLS pour toutes les connexions
- Authentification par certificat ou mot de passe
- Controle d'acces granulaire par variable
- Conformite aux profils de securite OPC UA

---

<div style="text-align:center; padding: 2rem;">

**Bellows est en cours de developpement. Les informations seront mises a jour
au fur et a mesure de l'avancement.**

blacksmith@forgeiec.io

</div>
