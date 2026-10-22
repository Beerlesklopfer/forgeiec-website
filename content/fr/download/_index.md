---
title: "Téléchargement"
summary: "Tous les composants ForgeIEC — dépôts APT et RPM, téléchargements directs, code source"
---

## Les composants ForgeIEC en un coup d'œil

ForgeIEC se compose de plusieurs composants. Ceux dont vous avez besoin
dépendent de votre rôle :

| Rôle | Composant | Où l'installer |
|---|---|---|
| **Programmeur / utilisateur d'automate** | `forgeiec-studio` | Poste de travail |
| **Ingénieur de mise en service** | `forgeiec-anvil-server` (fournit `anvild`) | Automate cible |
| **Passerelle IHM / OPC-UA** | `forgeiec-bellows-server` (fournit `bellowsd`) | Automate cible ou hôte séparé |
| **Modbus TCP** | inclus dans `forgeiec-anvil-server` | Automate cible |
| **Profibus / EtherCAT / EthernetIP** | également dans `forgeiec-anvil-server` | Automate cible |
| **Pupitre opérateur** | `forgeiec-screen-wayland` ou `-xorg` | Matériel du pupitre |

---

## Installation depuis le dépôt de paquets

ForgeIEC est fourni sous forme de dépôt Debian signé sur
`apt.forgeiec.io` et de dépôt RPM signé sur `rpm.forgeiec.io`.
La configuration se fait une seule fois par poste de travail ou
automate cible — choisissez votre distribution :

{{< distro-install >}}

Installez ensuite les composants individuellement :

```bash
# Poste de travail
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # Descriptions d'appareils (recommandé)

# Automate cible
sudo apt install forgeiec-anvil-server    # Runtime automate (anvild + tous les tongs-*)
sudo apt install forgeiec-bellows-server  # Passerelle IHM (bellowsd)

# Pupitre opérateur
sudo apt install forgeiec-screen-wayland  # Kiosque sous Wayland
sudo apt install forgeiec-screen-xorg     # Kiosque sous X11
```

Sur les systèmes RPM, les commandes s'écrivent `sudo dnf install …`
avec des noms de paquets identiques.

Les passerelles de bus (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) ne sont **pas** des paquets séparés — elles se trouvent
dans `forgeiec-anvil-server` et sont démarrées par `anvild`.

Les mises à jour suivent le cycle habituel `apt update && apt upgrade` —
aucun fichier `.deb` manuel n'est nécessaire.

---

## Plateformes prises en charge

### Debian / Ubuntu (`apt.forgeiec.io`)

| Paquet | Architectures | Suites |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | indépendant de l'architecture | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

Correspondance des suites : `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Paquet | Architecture | Distributions |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

La distribution RPM est récente et ne couvre pour l'instant que le
pupitre opérateur. ForgeIEC Studio et le runtime suivront dès que leurs
créneaux RPM seront stables.

Il existe **deux clés de signature différentes** : `forgeiec.gpg` (ed25519)
pour apt et `forgeiec-rpm.asc` (RSA-4096) pour rpm. La différence n'est
pas cosmétique — RHEL 9 fournit `rpm` 4.16, dont l'analyseur PGP interne
ne sait pas vérifier ed25519.

arm64 est volontairement absent côté RPM : la chaîne de compilation
croisée de la CI dépend de paquets Debian qui n'existent pas sous
Enterprise Linux.

**Version Windows** de ForgeIEC Studio : en préparation. D'ici là,
Studio fonctionne nativement sous Linux ou via WSL2 sur les postes
Windows.

---

## Téléchargements directs (archives de version)

Si vous ne pouvez pas ou ne voulez pas utiliser le dépôt de paquets — par
exemple pour des postes isolés (air gap) — vous pouvez obtenir les versions
individuelles depuis le Forgejo. **Les dépôts ne sont pas consultables
publiquement** : envoyez-nous votre clé publique SSH à
blacksmith@forgeiec.io et nous l'activerons. Les dépôts suivants vous
sont alors ouverts :

- **Source de ForgeIEC Studio** : `ForgeIEC/forgeiec-studio`
- **anvild + passerelles** : `ForgeIEC/anvil`
- **bellowsd** : `ForgeIEC/bellows`
- **Source du site web** : `ForgeIEC/forgeiec-website`

Pour chaque version, des paquets `.deb` signés et des archives source
sont joints au tag de version sur le Forgejo.

---

## Compilation depuis les sources

```bash
# Cloner le dépôt (avec sous-modules) — uniquement via SSH, une fois
# votre clé publique SSH activée
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# Compiler Studio + tous les démons
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# Déployer sur le système local
./deploy.sh all
```

Prérequis :

- Debian 12/13 ou Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+ (via rustup)

---

## Projets de démonstration

Projets d'exemple fournis avec ForgeIEC Studio :

| Projet | Objectif |
|---|---|
| `knight_rider.forge` | Test classique de chenillard pour les LED Bellows |
| d'autres à venir | … |

Dans Studio, sous `File → Open Example`.

---

## Étapes suivantes

- [Premiers pas avec ForgeIEC Studio](/help/)
- [Configurer l'assistant IA](/en/help/ai/) (en anglais)
- [Configuration du bus](/help/bus-config/)
- [Actualités + notes de version](/en/news/) (en anglais)
