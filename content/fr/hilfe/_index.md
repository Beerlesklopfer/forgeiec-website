---
title: "Aide"
summary: "Documentation et ressources pour ForgeIEC"
---

## Aide et ressources

Bienvenue dans la section d'aide de ForgeIEC. Vous trouverez ici des
informations sur les fondements de notre projet et de notre philosophie.

---

## Sujets

### [Configuration Bus](/hilfe/bus-config/)

Schema XML PLCopen pour la configuration des bus de terrain industriels
dans les projets `.forge`. Segments, appareils, liaison de variables et
attribution d'adresses IEC.

### [Couverture de tests](/hilfe/tests/)

117 tests automatises verifient l'ensemble complet du langage IEC 61131-3,
les 132 blocs de la bibliotheque standard et le systeme de threading multi-tache.

### [Philosophie Open Source](/hilfe/open-source/)

L'idee derriere l'open source va bien au-dela du logiciel — c'est un
mouvement qui libere le savoir et democratise l'innovation.

---

## Pour commencer

ForgeIEC se compose de deux composants :

1. **Editeur ForgeIEC** (`forgeiec`) — L'environnement de developpement sur votre poste de travail
2. **Daemon ForgeIEC** (`anvild`) — Le systeme d'execution sur l'automate cible

### Installation depuis le depot APT ForgeIEC

ForgeIEC est fourni sous forme de depot Debian signe a l'adresse
`apt.forgeiec.io`. La configuration s'effectue une seule fois sur
chaque poste de travail ou automate cible :

```bash
# Importer la cle de signature
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Ajouter la source du depot
# (Debian 12 "bookworm" ou Debian 13 "trixie" — selon votre systeme)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Ensuite, installez n'importe quel paquet ForgeIEC avec le gestionnaire
de paquets standard :

```bash
# Editeur (poste de travail)
sudo apt install forgeiec

# Daemon (automate cible)
sudo apt install anvild
```

Les mises a jour suivent le cycle normal `apt update && apt upgrade` —
aucun fichier `.deb` manuel n'est necessaire.

### Plateformes supportees

| Composant | Architectures | Versions Debian  |
|-----------|---------------|------------------|
| Editeur   | amd64, arm64  | bookworm, trixie |
| Daemon    | amd64, arm64  | bookworm, trixie |
| Bridges   | amd64, arm64  | bookworm, trixie |
| Hearth    | amd64, arm64  | bookworm, trixie |

### Contact

Pour toute question : blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**La documentation grandit avec le projet.**

blacksmith@forgeiec.io

</div>
