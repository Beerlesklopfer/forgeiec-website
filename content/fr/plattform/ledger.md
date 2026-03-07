---
title: "Ledger"
description: "Gestion des ordres de fabrication et integration MES"
weight: 7
---

## Ledger -- Gestion des ordres de fabrication

**En cours de developpement**

Ledger est le module de gestion des ordres de fabrication de la plateforme
ForgeIEC. Le registre du forgeron trace chaque piece produite -- Ledger trace
chaque ordre de fabrication, chaque etape de production et chaque resultat.

---

## Integration MES

Les systemes MES (Manufacturing Execution Systems) font le lien entre la
planification de production (ERP) et l'execution sur le terrain (automates).
Ledger fournira cette couche d'integration pour la plateforme ForgeIEC.

### Fonctionnalites planifiees

- **Gestion des ordres** -- Reception, lancement et suivi des ordres de fabrication
- **Suivi de production** -- Comptage des pieces, temps de cycle, taux de rendement
- **Tracabilite** -- Association des parametres de processus a chaque lot produit
- **Rapports de production** -- Generation automatique de rapports par poste, equipe ou periode
- **Interface ERP** -- Echange de donnees avec les systemes de planification existants

---

## Architecture prevue

Ledger fonctionnera comme un service independant, connecte au runtime via
Anvil (Zero-Copy IPC) pour les donnees de processus en temps reel, et via
une API REST pour l'integration avec les systemes IT.

### Integration dans la plateforme

- **Anvil** -- Donnees de processus en temps reel (compteurs, etats machine)
- **Hearth** -- Affichage des ordres de fabrication dans l'IHM
- **Bellows** -- Echange de donnees OPC UA avec les systemes MES tiers
- **Forge Studio** -- Configuration des variables de production depuis l'IDE

---

## Cas d'utilisation

### Fabrication discrete

Suivi des ordres de fabrication piece par piece, avec comptage automatique
et detection des rebuts base sur les signaux de l'automate.

### Industrie de process

Suivi des lots de production, enregistrement des parametres de processus
(temperature, pression, debit) et generation de rapports de lot.

### Maintenance

Compteurs d'heures de fonctionnement, cycles de maintenance preventive
et declenchement automatique des ordres de maintenance.

---

<div style="text-align:center; padding: 2rem;">

**Ledger est en cours de developpement. Les informations seront mises a jour
au fur et a mesure de l'avancement.**

blacksmith@forgeiec.io

</div>
