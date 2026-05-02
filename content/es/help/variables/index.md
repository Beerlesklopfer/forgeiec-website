---
title: "Gestión de variables"
summary: "El panel de variables como vista central sobre el FAddressPool — columnas, filtros, operaciones masivas, interruptores de seguridad"
---

## Visión general

El **panel de variables** es la vista central sobre el **FAddressPool**
— la única fuente de verdad para cada variable en un proyecto ForgeIEC.
Cada variable existe exactamente una vez en el pool, indexada por su
dirección IEC (`%IX0.0`, `%QW3`, ...). Contenedores como GVL,
AnvilVarList, HmiVarList o interfaces de POU son solo **vistas** sobre
este pool — ninguna variable vive en dos almacenes en paralelo.

```
FAddressPool  (single source of truth)
   |
   +-- FAddressPoolModel  (Qt table)
         |
         +-- FVariablesPanel  (filters + bulk ops + clipboard)
               |
               +-- Tree filter sets FilterMode + tag
```

El panel se acopla en la parte inferior de la ventana principal y
refleja cada cambio inmediatamente en cualquier otra vista (editor de
POU, compilador ST, guardado PLCopen-XML).

## Columnas

La tabla tiene **15 columnas**; cada una puede activarse o desactivarse
individualmente mediante el menú contextual del encabezado — cada
instancia del editor de POU almacena su visibilidad de columnas de
forma independiente.

| Columna | Contenido |
|---|---|
| **Nombre** | Nombre visible para el programador. Las entradas de pool cualificadas aparecen con su ruta completa: `Anvil.Pfirsich.T_1`, `Bellows.Stachelbeere.T_Off`, `GVL.Motor.K1_Mains`. |
| **Tipo** | Tipo elemental IEC o tipo definido por el usuario. Los arrays se muestran como `ARRAY [0..7] OF BOOL`. |
| **Dirección** | Var-class IEC: `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` para locales de POU; `in`/`out` para globales del pool (derivadas de `%I` vs. `%Q`). |
| **Address** | Dirección IEC — la clave primaria. `%IX0.0` para una entrada de bit, `%QW1` para una salida de palabra, `%MX10.3` para un bit de marca. |
| **Inicial** | Valor inicial (`FALSE`, `0`, `T#100ms`, `'OFF'`). Cargado en la variable en el primer ciclo. |
| **Dispositivo de bus** | UUID del dispositivo de bus (esclavo Modbus, etc.) al que está vinculada esta variable — editable como combo box. |
| **Bus Addr** | Desplazamiento del registro Modbus relativo al esclavo (`0`, `1`, ...). |
| **R** (Retain) | Casilla de verificación — ¿el valor sobrevive a un ciclo de alimentación? |
| **C** (Constant) | Casilla de verificación — constante IEC (`VAR CONSTANT`), valor no escribible en tiempo de ejecución. |
| **RO** (ReadOnly) | Casilla de verificación — solo lectura desde el código del programa. |
| **Sync** | Clase de sincronización multitarea (`L`/`A`/`D`), producida por la última ejecución del compilador ST. |
| **Used by** | Qué tareas leen/escriben esta variable, p. ej. `PROG_Fast (R/W), PROG_Slow (R)`. |
| **Monitor** / **HMI** / **Force** | Interruptores de seguridad por variable. **Cluster A** en el backlog — opt-ins explícitos, distintos de la etiqueta `hmiGroup`. El compilador ST verifica antes de la generación de código que el acceso Force/HMI solo apunta a variables que llevan el flag. |
| **Live** | Valor en tiempo de ejecución en modo online (alimentado por el almacén de valores en vivo de anvild; oculto cuando está desconectado). |
| **Scope** | Casilla de visibilidad para el osciloscopio — envía la variable al panel del osciloscopio. |
| **Documentation** | Comentario de texto libre. |

## Modos de filtro

El panel no muestra todo el pool de una vez — el **árbol del proyecto a
la izquierda** elige qué porción es visible. Hacer clic en un nodo del
árbol hace que la ventana principal establezca `FilterMode` más etiqueta:

| FilterMode | Muestra |
|---|---|
| `FilterAll` | Todo el pool — sin restricción de etiqueta. |
| `FilterByGvl` | Variables con `gvlNamespace == tag` (p. ej. solo `GVL.Motor`). |
| `FilterByAnvil` | Variables con `anvilGroup == tag` (un grupo Anvil IPC). |
| `FilterByHmi` | Variables con `hmiGroup == tag` (un grupo HMI Bellows). |
| `FilterByBus` | Variables con `busBinding.deviceId == tag` (todas las variables de un dispositivo de bus). |
| `FilterByModule` | Como `FilterByBus`, más `moduleSlot` — formato de etiqueta `hostname:slot`. |
| `FilterByPou` | Locales de POU — variables con `pouInterface == tag`. |
| `FilterCommentsOnly` | Solo separadores de comentarios, sin variables. |

## Ejes de filtro (componibles)

Sobre la tabla hay cuatro ejes adicionales que actúan todos en paralelo
sobre el filtro del árbol:

  - **Búsqueda de texto libre** sobre nombre, dirección y etiquetas — `to` encuentra `T_Off`.
  - **Filtro de tipo IEC** como combo (`all` / `BOOL` / `INT` / `REAL` / ...).
  - **Filtro de rango de direcciones**: `all` / `%I` (entradas) / `%Q` (salidas) /
    `%M` (marcas); dentro de `%M` además por tamaño de palabra (`%MX` / `%MW` /
    `%MD` / `%ML`).
  - **Conmutador TaggedOnly** — oculta cada entrada del pool sin
    ninguna etiqueta de contenedor (útil para encontrar un pool
    "huérfano").

Cada filtro se combina con AND: cualquier cosa que no coincida con
todos los ejes activos se oculta.

## Selección múltiple + operaciones masivas

Como en cualquier tabla Qt: Shift-clic y Ctrl-clic seleccionan rangos o
filas individuales. El menú contextual sobre la selección ofrece:

  - **Set Anvil Group...** — establece `anvilGroup` en cada variable seleccionada.
  - **Set HMI Group...** — lo mismo para `hmiGroup`.
  - **Set GVL Namespace...** — lo mismo para `gvlNamespace`.
  - **Clear Tag** — elimina la etiqueta del modo de filtro activo.
  - **Toggle Monitor / HMI / Force** — conmutación masiva de los
    interruptores de seguridad.

Cada edición masiva pasa por `FAddressPoolModel::applyToRows`, da como
resultado una única señal `dataChanged` y es deshacible como un único
paso de undo.

## Portapapeles (copiar / cortar / pegar)

Las variables seleccionadas pueden copiarse — **con todas las etiquetas
y flags** — y pegarse en otra vista. La carga útil utiliza dos formatos:

  - **MIME personalizado** (`application/x-forgeiec-vars+json`) como
    vehículo de ida y vuelta que lleva la información completa del pool.
  - **TSV de texto plano** como respaldo para Excel / editores de texto.

Al **pegar** el panel reapunta automáticamente las etiquetas de
contenedor al **modo de filtro activo**: copiar desde `FilterByAnvil`
(grupo `Pfirsich`) y pegar en `FilterByHmi` (grupo `Stachelbeere`) y
las variables descartan su `anvilGroup` y adoptan
`hmiGroup = Stachelbeere`. Las direcciones y nombres conflictivos se
deduplican (`T_1` → `T_1_1`).

## Arrastrar/soltar en HmiVarList

Las variables pueden arrastrarse desde el panel principal a una POU
HmiVarList. El editor establece entonces automáticamente el **flag de
exportación HMI** de la variable y escribe el grupo HMI como etiqueta
— la exportación a Bellows queda armada.

## Interruptores de seguridad por variable

Tres interruptores por variable, cada uno requiriendo un opt-in
explícito:

  - **HMI** — permite a Bellows leer/escribir la variable.
  - **Monitor** — permite la observación en vivo en modo online.
  - **Force** — permite forzar un valor en tiempo de ejecución.

Estos flags son **independientes de la etiqueta `hmiGroup`**. La
etiqueta describe la pertenencia al grupo; el flag activa el efecto.
Antes de cada generación de código, el compilador ST verifica que cada
acceso Bellows o Force apunte a una variable cuyo flag esté
establecido — de lo contrario, lanza un error de compilación.

## Temas relacionados

  - [Añadir una variable](add/) — el `FAddVariableDialog` con patrones
    de rango y el envoltorio de array.
  - [Formato de archivo de proyecto](../file-format/) — cómo se
    persiste el pool como bloque `<addData>` en PLCopen XML.
  - [Biblioteca](../library/) — cómo los bloques de función ven sus
    instancias en el pool.
