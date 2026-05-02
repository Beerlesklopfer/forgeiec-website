---
title: "Éditeur Sequential Function Chart (SFC)"
summary: "Modèle étape-transition pour le contrôle séquentiel et les machines à modes"
---

## Vue d'ensemble

Sequential Function Chart (SFC) est le troisième langage graphique
IEC 61131-3 et décrit des **séquences orientées état** via un modèle
étape-transition — formellement apparenté aux réseaux de Petri. Un
diagramme SFC est constitué d'une séquence d'**étapes** connectées par
des **transitions** avec conditions. À tout moment, un sous-ensemble
des étapes est actif ; une étape est quittée lorsque sa transition
sortante devient TRUE.

SFC est le langage naturel pour le **contrôle séquentiel, les machines
à modes et les processus par lots** — tout ce que vous décririez comme
« d'abord ceci, puis cela, sauf quand ... ».

## Disposition de l'éditeur

L'éditeur SFC suit le même schéma en trois parties que FBD et LD :
barre d'outils en haut, QGraphicsView avec grille + zoom + panoramique,
tableau de variables à droite. La barre d'outils propose des outils
pour chaque type d'élément SFC.

## Types d'éléments

### Étape

Une étape est une **boîte rectangulaire** avec un nom. Tant qu'elle est
active, les actions qui lui sont associées s'exécutent.

* **Étape initiale :** le point d'entrée du POU. Devient active au
  démarrage du programme. Dessinée avec une **double bordure** dans
  l'éditeur.
* **Étapes suivantes :** dessinées avec une bordure simple. Deviennent
  actives lorsque la transition précédente se déclenche.

Ports : haut (IN, depuis la transition précédente), bas (OUT, vers la
transition suivante), droite (connexion vers les blocs d'action).

### Transition

Une transition est une **courte barre horizontale** sur la ligne de
connexion verticale entre deux étapes. À droite de la barre se trouve
la **condition** — soit une expression ST (par ex. `tmr.Q AND xReady`),
soit la sortie d'un bloc fonctionnel.

Lorsque la condition devient TRUE, l'étape précédente est désactivée
et l'étape suivante devient active.

### Bloc d'action

Un bloc d'action décrit **ce qui se passe pendant qu'une étape est
active**. Il est constitué de deux cellules : le **qualificateur** à
gauche et le **nom de l'action** à droite (une référence à une action
ST ou à une variable de sortie).

| Qualificateur | Signification |
|---|---|
| `N` | Non-stocké — s'exécute tant que l'étape est active (par défaut). |
| `P` | Pulse — se déclenche une fois pendant un cycle à l'activation de l'étape. |
| `S` | Set — défini et reste actif à travers les transitions d'étape. |
| `R` | Reset — efface une action préalablement définie avec `S`. |
| `L` | Limited — s'exécute pendant la durée donnée au maximum. |
| `D` | Delayed — démarre seulement après le délai donné. |

Plusieurs blocs d'action peuvent être attachés à une étape.

### Divergence et convergence

Une **divergence** ramifie la séquence en plusieurs chemins, une
**convergence** les rejoint à nouveau. SFC en a deux types :

* **Sélection (divergence OR) :** **exactement un** des chemins est
  emprunté, selon quelle condition de transition devient TRUE en
  premier. Dessinée comme une **barre horizontale simple**.
* **Parallèle (divergence AND) :** **tous** les chemins deviennent
  actifs simultanément et s'exécutent indépendamment. Ce n'est que
  lorsque chacun atteint le point de convergence que la séquence
  avance. Dessinée comme une **barre horizontale double**.

### Saut

Un élément de saut est une **flèche vers le bas** portant le nom de
l'étape cible. Il transfère le contrôle du chemin courant vers une
étape nommée — typiquement utilisé pour « retour au début » à la fin
d'une séquence, ou pour la gestion d'erreur (« sauter à
`Step_Error` »).

## Application

SFC convient chaque fois qu'un programme a une **séquence temporelle**
claire :

* **Modes de machine** — Init → Idle → Running → Cleanup → Idle.
* **Processus par lots** — Remplissage → Chauffage → Mélange → Vidange.
* **Séquences de sécurité** — exécuter des séquences d'arrêt dans un
  ordre défini (« d'abord chauffage off, puis pompe off, puis
  contacteur principal »).
* **Génie des procédés** — étapes de réaction avec délais et
  conditions.

Comparée à une implémentation ST de la même fonction, la version SFC
est sensiblement plus lisible — l'ordre des étapes et les conditions
de branchement sont graphiquement évidents, alors qu'en ST une
construction `CASE state OF` ne transmet la même information
qu'indirectement.

## Sujets liés

* [Function Block Diagram](../fbd/) — pour la logique **à l'intérieur**
  d'une action ou d'une condition de transition.
* [Ladder Diagram](../ld/) — langage graphique alternatif pour des
  circuits de verrouillage plus simples.
* [Bibliothèque](../library/) — les temporisateurs (`TON`, `TP`) sont
  des composants courants des conditions de transition.
