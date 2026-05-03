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

Les principaux sujets sont listes dans l'[apercu de l'aide](/help/).

## Dans l'editeur

- **F1** sur un element actif → page d'aide contextuelle
- **Aide → Aide en ligne** dans le menu principal → point d'entree (cette page)
- **Aide → A propos de ForgeIEC** → version + licence
