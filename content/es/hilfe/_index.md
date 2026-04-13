---
title: "Ayuda"
summary: "Documentacion y recursos para ForgeIEC"
---

## Ayuda y recursos

Bienvenido a la seccion de ayuda de ForgeIEC. Aqui encontrara informacion
sobre los fundamentos de nuestro proyecto y nuestra filosofia.

---

## Temas

### [Configuracion de Bus](/hilfe/bus-config/)

Esquema XML PLCopen para la configuracion de buses de campo industriales
en proyectos `.forge`. Segmentos, dispositivos, vinculacion de variables
y asignacion de direcciones IEC.

### [Cobertura de pruebas](/hilfe/tests/)

117 pruebas automatizadas verifican el conjunto completo del lenguaje IEC 61131-3,
los 132 bloques de la biblioteca estandar y el sistema de threading multi-tarea.

### [Filosofia Open Source](/hilfe/open-source/)

La idea detras del codigo abierto va mucho mas alla del software — es un
movimiento que libera el conocimiento y democratiza la innovacion.

---

## Primeros pasos

ForgeIEC consta de dos componentes:

1. **Editor ForgeIEC** (`forgeiec`) — El entorno de desarrollo en su estacion de trabajo
2. **Daemon ForgeIEC** (`anvild`) — El sistema de ejecucion en el PLC destino

### Instalacion desde el repositorio APT de ForgeIEC

ForgeIEC se proporciona como un repositorio Debian firmado en
`apt.forgeiec.io`. La configuracion se realiza una sola vez en
cada estacion de trabajo o PLC destino:

```bash
# Importar clave de firma
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Agregar fuente del repositorio
# (Debian 12 "bookworm" o Debian 13 "trixie" — segun su sistema)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Luego instale cualquier paquete ForgeIEC con el gestor de paquetes
estandar:

```bash
# Editor (estacion de trabajo)
sudo apt install forgeiec

# Daemon (PLC destino)
sudo apt install anvild
```

Las actualizaciones siguen el ciclo normal de `apt update && apt upgrade` —
no se necesitan archivos `.deb` manuales.

### Plataformas soportadas

| Componente | Arquitecturas | Versiones Debian |
|------------|---------------|------------------|
| Editor     | amd64, arm64  | bookworm, trixie |
| Daemon     | amd64, arm64  | bookworm, trixie |
| Bridges    | amd64, arm64  | bookworm, trixie |
| Hearth     | amd64, arm64  | bookworm, trixie |

### Contacto

Para preguntas: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**La documentacion crece con el proyecto.**

blacksmith@forgeiec.io

</div>
