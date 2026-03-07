---
title: "Hearth"
description: "SCADA/IHM pour la visualisation de processus industriels"
weight: 4
---

## Hearth -- SCADA/IHM

**En cours de developpement**

Hearth est le systeme de supervision et d'interface homme-machine de la
plateforme ForgeIEC. Le foyer est le coeur de la forge, la ou le feu brule --
Hearth est le coeur de la supervision, la ou les processus sont visualises.

---

## Visualisation de processus

Les systemes d'automatisation industrielle necessitent une interface de
supervision pour observer, commander et diagnostiquer les processus de
production. Hearth fournira cette couche de visualisation.

### Fonctionnalites planifiees

- **Tableaux de bord en temps reel** -- Visualisation des variables de processus avec mise a jour en direct
- **Synoptiques** -- Representation graphique des installations avec symboles industriels
- **Historique des donnees** -- Enregistrement et affichage des tendances sur le long terme
- **Gestion des alarmes** -- Detection, notification et acquittement des alarmes
- **Rapports** -- Generation de rapports de production automatises

---

## Architecture prevue

Hearth fonctionnera comme une application web, accessible depuis n'importe
quel navigateur sur le reseau. Les donnees de processus seront recues via
OPC UA (Bellows) ou directement via gRPC depuis le runtime.

### Composants planifies

- Interface web responsive (desktop et tablette)
- Editeur de synoptiques integre
- Moteur d'alarmes configurable
- Base de donnees historique
- Systeme de droits et profils utilisateurs

---

## Integration dans la plateforme

Hearth s'integrera avec les autres composants de la plateforme ForgeIEC :

- **Anvil** -- Donnees de processus en temps reel
- **Bellows** -- Communication OPC UA standard
- **Ledger** -- Donnees de production et ordres de fabrication
- **Forge Studio** -- Configuration depuis l'IDE

---

<div style="text-align:center; padding: 2rem;">

**Hearth est en cours de developpement. Les informations seront mises a jour
au fur et a mesure de l'avancement.**

blacksmith@forgeiec.io

</div>
