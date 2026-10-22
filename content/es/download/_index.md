---
title: "Descargas"
summary: "Todos los componentes de ForgeIEC — repositorios APT y RPM, descargas directas, código fuente"
---

## Los componentes de ForgeIEC de un vistazo

ForgeIEC consta de varios componentes. Cuáles necesita depende de su
función:

| Función | Componente | Dónde instalarlo |
|---|---|---|
| **Programador / usuario de PLC** | `forgeiec-studio` | Estación de trabajo |
| **Ingeniero de puesta en marcha** | `forgeiec-anvil-server` (incluye `anvild`) | PLC de destino |
| **Pasarela HMI / OPC-UA** | `forgeiec-bellows-server` (incluye `bellowsd`) | PLC de destino o equipo aparte |
| **Modbus TCP** | incluido en `forgeiec-anvil-server` | PLC de destino |
| **Profibus / EtherCAT / EthernetIP** | también en `forgeiec-anvil-server` | PLC de destino |
| **Panel de operador** | `forgeiec-screen-wayland` o `-xorg` | Hardware del panel |

---

## Instalación desde el repositorio de paquetes

ForgeIEC se distribuye como repositorio Debian firmado en
`apt.forgeiec.io` y como repositorio RPM firmado en
`rpm.forgeiec.io`. La configuración se hace una sola vez por estación
de trabajo o PLC de destino — elija su distribución:

{{< distro-install >}}

Después instale los componentes por separado:

```bash
# Estación de trabajo
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # Descripciones de dispositivos (recomendado)

# PLC de destino
sudo apt install forgeiec-anvil-server    # Runtime de PLC (anvild + todos los tongs-*)
sudo apt install forgeiec-bellows-server  # Pasarela HMI (bellowsd)

# Panel de operador
sudo apt install forgeiec-screen-wayland  # Quiosco en Wayland
sudo apt install forgeiec-screen-xorg     # Quiosco en X11
```

En sistemas RPM los comandos son `sudo dnf install …` con los mismos
nombres de paquete.

Las pasarelas de bus (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) **no** son paquetes independientes — están dentro de
`forgeiec-anvil-server` y las inicia `anvild`.

Las actualizaciones siguen el ciclo habitual `apt update && apt upgrade` —
no hace falta manejar archivos `.deb` a mano.

---

## Plataformas compatibles

### Debian / Ubuntu (`apt.forgeiec.io`)

| Paquete | Arquitecturas | Suites |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | independiente de la arquitectura | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

Correspondencia de suites: `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Paquete | Arquitectura | Distribuciones |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

La distribución RPM es nueva y por ahora solo cubre el panel de operador.
ForgeIEC Studio y el runtime llegarán en cuanto sus paquetes RPM sean
estables.

Hay **dos claves de firma distintas**: `forgeiec.gpg` (ed25519) para apt
y `forgeiec-rpm.asc` (RSA-4096) para rpm. La diferencia no es estética —
RHEL 9 incluye `rpm` 4.16, cuyo analizador PGP interno no puede verificar
ed25519.

arm64 falta a propósito en el lado RPM: la compilación cruzada de la CI
depende de paquetes Debian que no existen en Enterprise Linux.

**Versión para Windows** de ForgeIEC Studio: en preparación. Mientras
tanto, Studio funciona de forma nativa en Linux o mediante WSL2 en
estaciones Windows.

---

## Descargas directas (tarballs de versión)

Si no puede o no quiere usar el repositorio de paquetes — por ejemplo en
estaciones aisladas (air gap) — puede obtener versiones concretas desde el
Forgejo. **Los repositorios no se pueden consultar públicamente**: envíenos
su clave pública SSH a blacksmith@forgeiec.io y la habilitaremos. A partir
de entonces tendrá acceso a estos repositorios:

- **Código fuente de ForgeIEC Studio**: `ForgeIEC/forgeiec-studio`
- **anvild + pasarelas**: `ForgeIEC/anvil`
- **bellowsd**: `ForgeIEC/bellows`
- **Código fuente del sitio web**: `ForgeIEC/forgeiec-website`

En cada versión se adjuntan paquetes `.deb` firmados y tarballs de código
fuente a la etiqueta de versión en el Forgejo.

---

## Compilar desde el código fuente

```bash
# Clonar el repositorio (con submódulos) — solo por SSH, una vez
# habilitada su clave pública SSH
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# Compilar Studio + todos los daemons
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# Desplegar en el sistema local
./deploy.sh all
```

Requisitos:

- Debian 12/13 o Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+ (mediante rustup)

---

## Proyectos de demostración

Proyectos de ejemplo incluidos con ForgeIEC Studio:

| Proyecto | Propósito |
|---|---|
| `knight_rider.forge` | Prueba clásica de luces secuenciales para los LED de Bellows |
| habrá más | … |

En Studio, en `File → Open Example`.

---

## Próximos pasos

- [Primeros pasos con ForgeIEC Studio](/help/)
- [Configurar el asistente de IA](/en/help/ai/) (en inglés)
- [Configuración del bus](/help/bus-config/)
- [Noticias + notas de versión](/en/news/) (en inglés)
