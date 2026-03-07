---
title: "Forge Studio"
description: "Environnement de developpement IEC 61131-3 -- IDE professionnel pour la programmation d'automates"
weight: 1
---

## Forge Studio -- L'IDE pour l'automatisation industrielle

Forge Studio est l'environnement de developpement integre de ForgeIEC pour la
programmation d'automates conformement a la norme IEC 61131-3. Developpe en
C++17 avec Qt6, il offre un outil de qualite industrielle pour toutes les
taches de programmation d'automates.

---

## Les cinq langages IEC 61131-3

Un seul editeur pour tous les langages -- commutation transparente, variables
partagees, structure de projet unifiee.

- **Texte structure (ST)** -- Coloration syntaxique, auto-completion, rechercher et remplacer
- **Liste d'instructions (IL)** -- Support complet du langage avec edition intelligente
- **Diagramme de blocs fonctionnels (FBD)** -- Editeur graphique avec bibliotheque de blocs
- **Schema a contacts (LD)** -- Representation familiere pour la logique de commutation
- **Graphe fonctionnel sequentiel (SFC)** -- Diagrammes de sequences pour les commandes de processus

---

## Compilation et deploiement

Forge Studio compile les programmes IEC localement sur le poste de travail.
Les fichiers C generes sont transferes vers l'automate cible via gRPC chiffre.
L'automate n'a besoin que d'un compilateur C -- aucun compilateur IEC n'est
requis sur le systeme cible.

- Compilation locale avec `iec2c` (IEC 61131-3 vers C)
- Transfert chiffre vers le systeme cible
- Generation automatique du Makefile adapte a la plateforme
- Support des architectures x86_64, ARM64 et ARMv7

---

## Systemes de bus industriels

Configuration des bus de terrain dans le style CoDeSys avec hierarchie de
segments et detection automatique des peripheriques.

- **Modbus TCP** -- Communication Ethernet
- **Modbus RTU** -- Connexion serie RS-485
- **EtherCAT** -- Bus de terrain Ethernet temps reel
- **Profibus DP** -- Standard industriel eprouve
- Attribution automatique des adresses IEC sans conflits
- Scanner reseau pour la decouverte de peripheriques

---

## Debogage en direct

- Observation des variables en temps reel pendant l'execution de l'automate
- Forcage de valeurs sans arret de production
- Panneau de monitoring avec fonction de filtre

---

## Bibliotheque standard

Bibliotheque standard IEC complete : compteurs, temporisateurs, detection de
fronts, conversions de types et fonctions mathematiques. Extensible avec des
blocs definis par l'utilisateur. Stockee dans une base SQLite pour un acces
rapide et une recherche performante.

---

## Gestion des utilisateurs

- Authentification par mot de passe avec chiffrement bcrypt
- Tokens JWT pour les sessions
- Premier login dans le style CoDeSys
- Controle d'acces base sur les roles

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio -- Programme pour l'industrie. Open Source.**

blacksmith@forgeiec.io

</div>
