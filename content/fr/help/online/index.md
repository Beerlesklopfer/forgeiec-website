---
title: "Aide en ligne"
summary: "Point d'entree pour l'aide contextuelle depuis l'editeur ForgeIEC"
---

## Aide en ligne — Qu'est-ce que c'est ?

L'aide en ligne est la couche d'aide contextuelle de l'editeur ForgeIEC.
Appuyer sur **F1** dans l'editeur ouvre directement votre navigateur sur
la page d'aide de l'element actuellement actif (dialogue, panneau,
tableau de variables, action de generation de code, ...).

## Schema d'URL

Toutes les pages d'aide vivent sous un schema uniforme :

```
https://forgeiec.io/<langue>/help/<sujet>/
```

- `<langue>` suit la locale de l'editeur (de, en, fr, es, ja, tr, zh, ar) ;
  par defaut `de` si aucune page localisee n'existe
- `<sujet>` est un slug identique dans toutes les langues, non traduit

Vous pouvez donc ouvrir une page d'aide directement dans votre
navigateur sans demarrer l'editeur.

## Sujets disponibles

### Editeur & langages

- [Structured Text (ST)](/fr/help/st/) — Editeur ST + fondamentaux du langage
- [Instruction List (IL)](/fr/help/il/) — langage IEC base sur accumulateur
- [Function Block Diagram (FBD)](/fr/help/fbd/) — cablage graphique de fonctions et blocs fonctionnels
- [Ladder Diagram (LD)](/fr/help/ld/) — metaphore du schema electrique : contacts, bobines
- [Sequential Function Chart (SFC)](/fr/help/sfc/) — modele etape-transition pour sequenceurs

### Modele & variables

- [Gestion des variables](/fr/help/variables/) — panneau Variables comme vue centrale du FAddressPool
- [Bibliotheque](/fr/help/library/) — bibliotheque standard IEC + extensions ForgeIEC + blocs definis par l'utilisateur
- [Panneau des proprietes](/fr/help/properties-panel/) — editeur inline pour l'element bus selectionne
- [Preferences](/fr/help/preferences/) — dialogue de configuration central : editeur, runtime, automate, assistant IA

### Bus & materiel

- [Configuration du bus](/fr/help/bus-config/) — schema XML PLCopen pour la configuration des bus de terrain industriels

### General

- [Couverture des tests](/fr/help/tests/) — 117 tests automatises pour le jeu de fonctionnalites IEC, les blocs standard et le multi-tasking
- [Philosophie Open Source](/fr/help/open-source/) — contexte

## Dans l'editeur

- **F1** sur un element actif → page d'aide contextuelle
- **Aide → Aide en ligne** dans le menu principal → point d'entree (cette page)
- **Aide → A propos de ForgeIEC** → version + licence
