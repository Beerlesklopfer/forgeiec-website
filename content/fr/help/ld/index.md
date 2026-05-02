---
title: "Éditeur Ladder Diagram (LD)"
summary: "Métaphore du schéma de circuit : rails d'alimentation, contacts, bobines"
---

## Vue d'ensemble

Ladder Diagram (LD) est le plus ancien des trois langages graphiques
IEC 61131-3 et suit la **métaphore du schéma de circuit** : entre un
**rail d'alimentation** gauche et droit, des **chemins de courant**
(rungs) horizontaux portent le signal. Sur chaque rung, des contacts
sont à gauche (en série) et des bobines à droite ; selon l'état de la
variable, ils « passent » ou « bloquent » le courant. LD est bien
adapté à la logique de commande simple — fins de course, circuits
auto-maintenus, verrouillages — et est très lisible pour les
électriciens-concepteurs.

## Disposition de l'éditeur

L'éditeur LD a la même structure que l'éditeur FBD (barre d'outils en
haut, QGraphicsView avec grille + zoom + panoramique, tableau de
variables à droite), avec deux spécificités :

* Le **rail d'alimentation gauche** et le **rail d'alimentation
  droit** sont des éléments permanents dans le diagramme. Ils ne
  peuvent pas être déplacés et grandissent verticalement avec le nombre
  de rungs.
* La barre d'outils ajoute des boutons pour les symboles LD (contacts,
  bobines, déclencheurs de fronts) et un bouton `Add Rung` qui insère
  une nouvelle connexion de rung entre les rails d'alimentation.

## Symboles

### Contacts (côté gauche du rung)

| Symbole | Signification |
|---|---|
| `--\| \|--` | **Contact NO** — passe quand la variable est TRUE |
| `--\|/\|--` | **Contact NC** — passe quand la variable est FALSE |
| `--\|P\|--` | **Contact à front montant** — passe pendant un cycle sur un front montant |
| `--\|N\|--` | **Contact à front descendant** — passe pendant un cycle sur un front descendant |

Les contacts en série agissent comme un **AND** logique, les chemins
parallèles comme un **OR** logique.

### Bobines (côté droit du rung)

| Symbole | Signification |
|---|---|
| `--( )` | **Bobine standard** — écrit l'état du chemin de courant dans la variable |
| `--(/)` | **Bobine inversée** — écrit l'état inversé |
| `--(S)` | **Bobine Set** — met la variable à TRUE et la verrouille (même si le chemin s'ouvre plus tard) |
| `--(R)` | **Bobine Reset** — met la variable à FALSE et la verrouille |

Les paires set/reset implémentent un circuit auto-maintenu sans
logique IF-THEN explicite.

### Blocs fonctionnels sur le rung

Les fonctions et blocs fonctionnels de la bibliothèque peuvent être
insérés **en ligne entre contacts et bobines**. L'éditeur LD les
dessine comme une boîte horizontale avec des listes de broches à
droite et à gauche — sémantiquement identique au bloc FBD. Usages
typiques : temporisateurs (`TON`), compteurs (`CTU`), comparateurs
(`GT`, `EQ`).

## Exemple — circuit auto-maintenu avec priorité d'arrêt

Un circuit à relais classique : un bouton de démarrage `xStart` allume
un moteur `qMotor`, un bouton d'arrêt `xStop` l'éteint. Tant que
`xStart` a été pressé au moins une fois et que `xStop` n'est pas
pressé, le moteur reste allumé (auto-maintenu).

```text
        |                                              |
        |   xStart      xStop                          |
   +----| |---+--|/|---+-----------------------( )----+
        |    |         |                       qMotor  |
        |    |         |                                |
        |   qMotor     |                                |
        +----| |-------+                                |
        |                                              |
```

Lecture sous forme de phrase :

  * `xStart` (NO) **ou** `qMotor` (contact d'auto-maintien, NO) — en
    parallèle,
  * **et** `xStop` (NC) — en série,
  * pilotent la bobine `qMotor`.

À la compilation, le compilateur LD traduit ce rung en :

```text
qMotor := (xStart OR qMotor) AND NOT xStop;
```

C'est la forme la plus simple d'un latch avec priorité d'arrêt. Si les
deux boutons sont pressés en même temps, `xStop` gagne car le contact
NC ouvre le chemin.

## Sujets liés

* [Function Block Diagram](../fbd/) — langage sœur orienté flux de
  données.
* [Bibliothèque](../library/) — blocs fonctionnels pour usage en ligne
  sur le rung (`TON`, `CTU`, `JK_FF`, `DEBOUNCE`).
* [Panneau Variables](../variables/) — pool d'adresses et binding de
  variables.
