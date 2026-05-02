---
title: "Préférences"
summary: "Boîte de dialogue centrale de configuration de l'éditeur : Editor, Runtime, PLC, AI Assistant"
---

## Vue d'ensemble

La **boîte de dialogue Préférences** est le point d'entrée unique pour
tous les paramètres globaux à l'éditeur — tout ce qui *n'est pas* dans
le projet ouvert mais qui configure plutôt l'éditeur lui-même, la
connexion à un runtime, et le comportement post-upload.

Ouvrez la boîte de dialogue via **`Edit > Preferences...`** (certains
thèmes la placent sous `Tools > Preferences...`). Appuyez sur **F1**
lorsque la boîte de dialogue a le focus pour ouvrir cette page
directement.

```
Preferences
+-- Editor          (font, tab width, line numbers)
+-- Runtime         (anvild host/port, Anvil debug, network scanner)
+-- PLC             (build mode, auto-start, persist, monitoring)
+-- AI Assistant    (LLM endpoint, tokens, temperature)
```

## Editor

Contrôle l'apparence du texte dans l'éditeur de code ST et chaque
autre champ de saisie de texte.

| Champ | Signification |
|---|---|
| **Font**         | Famille de police. Pré-filtrée sur les polices monospace (recommandé : `JetBrains Mono`, `Cascadia Code`, `Consolas`). |
| **Font size**    | Taille de police en points. Par défaut `10`. |
| **Tab width**    | Nombre d'espaces par tabulation. Par défaut `4`. |
| **Show line numbers** | Affiche les numéros de ligne courants dans la gouttière de l'éditeur de code. |

## Runtime

Connexion à un démon **anvild** et diagnostic IPC.

| Champ | Signification |
|---|---|
| **Host**         | Nom d'hôte ou IP de l'automate. Par défaut `localhost`. |
| **Port**         | Port gRPC d'anvild. Par défaut `50051`. |
| **User**         | Nom d'utilisateur pour l'authentification par token. |
| **Anvil Debug**  | Niveau de diagnostic IPC (`Off`, `Errors only`, `Verbose`). Ajoute des statistiques supplémentaires au journal anvild — utile pour traquer la dérive de topic Iceoryx en production. |

De plus : **Auto-Connect on start** se connecte automatiquement au
dernier anvild connecté avec succès au démarrage de l'éditeur — pratique
sur un ordinateur portable d'ingénierie dédié.

Le bloc **Network Scanner** sur le même onglet scanne le LAN à la
recherche de périphériques Modbus TCP (port 502) et de runtimes
ForgeIEC (port 50051) et insère les résultats dans la configuration du
bus.

## PLC

Contrôle ce qui se passe après un **Upload** vers l'automate.

| Champ | Signification |
|---|---|
| **Compile Mode** | `Development` (monitoring en direct + forçage activés) ou `Production` (binaire dépouillé, pas de ponts de débogage — frontière de sécurité). |
| **PLC autostart**| Démarre automatiquement le runtime automate après un upload réussi, en sautant la boîte de dialogue de confirmation. |
| **Persist enabled** | Active la persistance périodique des variables `VAR_PERSIST`/`RETAIN` vers `/var/lib/anvil/persistent.dat`. Les valeurs survivent à un redémarrage du runtime. |
| **Persist polling interval** | Secondes entre les passes de sauvegarde automatique (par défaut `5 s`). |
| **Monitor history** | Nombre d'échantillons par variable dans l'enregistreur d'oscilloscope (par défaut `1000`). |
| **Monitor interval**| Intervalle d'échantillonnage en millisecondes pour le monitoring en direct (par défaut `100 ms`). |

## Library

Comportement de synchronisation pour la bibliothèque standard entre la
ressource de l'éditeur et le chemin de bibliothèque côté automate —
voir [Bibliothèque](../library/) pour le modèle complet de dérive. Deux
modes :

  - **Auto-Push off** (par défaut) — à la connexion, l'éditeur se
    contente de logger un indice dans le panneau de sortie quand une
    dérive est détectée. Le push se fait manuellement via
    `Tools > Sync Library`.
  - **Auto-Push on** — à chaque dérive détectée, l'éditeur pousse sa
    version locale de la bibliothèque automatiquement. Utile dans une
    configuration mono-programmeur.

## AI Assistant

Complétion de code optionnelle contre un serveur LLM local
compatible OpenAI (LM Studio, Ollama, llama.cpp, vLLM).

| Champ | Signification |
|---|---|
| **Enable AI Assistant** | Bascule la complétion en ligne. |
| **API Endpoint**        | Point de terminaison compatible OpenAI, par ex. `http://localhost:1234/v1`. |
| **Max Tokens**          | Limite de réponse par requête. Par défaut `2048`. |
| **Temperature**         | `Precise (0.1)`, `Balanced (0.3)`, `Creative (0.7)`, `Wild (1.0)`. |

## État UX (auto-persisté)

Les champs suivants sont stockés en arrière-plan **sans** passer par
la boîte de dialogue Préférences, pour que l'éditeur rouvre dans
l'état exact dans lequel vous l'avez quitté :

  - Géométrie et état de la fenêtre (`windowGeometry`, `windowState`)
  - Positions du splitter et des en-têtes (`splitterState`,
    `headerState`)
  - Hauteur du panneau de sortie (`outputPanelHeight`)
  - Dernier projet ouvert (`lastProject`) et liste des fichiers récents
  - État de session : onglets de POU ouverts, onglet actif, position du
    curseur et du défilement par POU

## Stockage des paramètres

Les paramètres sont stockés via `QSettings` de Qt, spécifique à la
plateforme :

| Plateforme | Chemin |
|---|---|
| **Windows** | Registre : `HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

Supprimer ce fichier / cette clé de registre réinitialise tous les
paramètres aux valeurs par défaut — utile après une mise à jour
ratée.

## Extensions planifiées

Backlog (cluster R phase 3) : le panneau de sortie aura ses propres
couleurs de sévérité (rouge erreur, jaune avertissement, blanc info) et
une taille de police configurable. Les deux options apparaîtront alors
ici sur un nouvel onglet `Output`.

## Sujets liés

  - [Bibliothèque](../library/) — comportement de synchronisation entre
    éditeur et runtime.
  - [Configuration du bus](../bus-config/) — paramètres au niveau
    projet qui *ne* vivent *pas* ici mais sur le segment / périphérique
    de bus lui-même.
