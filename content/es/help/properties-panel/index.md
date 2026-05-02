---
title: "Panel de propiedades"
summary: "Editor en línea para el elemento de bus seleccionado en el árbol del proyecto"
---

## Visión general

El **panel de propiedades** es la vista de detalle del lado derecho de
la ventana principal del editor. Muestra **todos los campos del
elemento actualmente seleccionado en el árbol del proyecto** y los hace
editables en línea — no es necesario abrir un diálogo modal para cada
edición.

```
Project tree                          Properties panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- click   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

Un **clic simple** sobre un nodo del árbol renderiza inmediatamente la
lista de campos correspondiente — un **doble clic** abre adicionalmente
el diálogo de configuración modal ([Configuración de bus](../bus-config/))
con exactamente el mismo conjunto de campos.

El panel está envuelto en un `QScrollArea` y se desplaza
verticalmente: los dispositivos con extensiones FDD más la tabla de
estado alcanzan fácilmente más de 40 campos, y todos deben permanecer
accesibles incluso cuando el dock es estrecho.

## Segmento de bus

Cuando se selecciona un segmento de bus, el panel muestra:

| Campo | Significado |
|---|---|
| **Name** | Nombre mostrado en el árbol del proyecto. |
| **Protocol** | `modbustcp`, `modbusrtu`, `ethercat`, `profibus`, `ethernetip`. |
| **Interface** | Interfaz de red a la que se vincula el puente (`eth0`, `eth1`, …). |
| **Bind Address** | Notación CIDR, p. ej. `192.168.1.10/24`. Validado. |
| **Gateway** | Pasarela predeterminada para el proceso del puente. |
| **Poll Interval** | Período en `ms` al que el puente sondea sus dispositivos. |
| **Enabled** | Si el subproceso del puente está activo. |

### Red avanzada (todo opcional)

Refleja el mismo grupo en `FSegmentDialog` y anula los valores
predeterminados del SO / puente:

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count** (heartbeat TCP)
  - **Max Connections** (`0` = ilimitado)
  - **VLAN ID** (`0` = sin etiqueta)

### Específico del protocolo

| Protocolo | Campos |
|---|---|
| `modbustcp`  | `Port` (predeterminado `502`), `Timeout` en `ms` (predeterminado `2000`). |
| `modbusrtu`  | `Serial Port` (p. ej. `/dev/ttyUSB0`), `Baud Rate`, `Parity` (`none`/`even`/`odd`). |
| `profibus`   | `Serial Port`, `Baud Rate` (hasta 12 Mbit/s), `Master Address` (0..126). |

### Logging

  - **Log Level** — `off` / `error` / `warn` / `info` / `debug`.
  - **Log File** — p. ej. `/var/log/forgeiec/segment.log`. Vacío = stdout.

## Dispositivo de bus

| Campo | Significado |
|---|---|
| **Hostname** | Nombre DNS o de visualización. |
| **IP Address** | IPv4 del dispositivo. |
| **Port** | Puerto Modbus en el esclavo (predeterminado `502`). |
| **Slave ID** | ID de unidad Modbus (0..247). |
| **Anvil Group** | Nombre del grupo Anvil IPC — también el nombre del `AnvilVarList` autogenerado. Renombrarlo renombra de forma sincronizada la etiqueta GVL, el AnvilVarList y cada variable del pool con `anvilGroup = oldGroup`. |

### Anulaciones avanzadas (todo opcional, vacío = heredar del segmento)

  - **MAC Address** — `AA:BB:CC:DD:EE:FF`. Validado.
  - **Endianness** — `ABCD` / `DCBA` / `BADC` / `CDAB`.
  - **Timeout** en `ms`. `0` = heredar del segmento.
  - **Retry Count**. `0` = heredar del segmento.
  - **Connection Mode** — `always connected` o `on demand`.
  - **Gateway (override)** — solo cuando el dispositivo vive en una subred diferente.
  - **Description** — texto libre (p. ej. `South irrigation valve`).

### Variables de estado (solo lectura)

Cada dispositivo expone automáticamente el modelo de fallos común —
siete campos implícitos publicados como un tópico de estado de solo
lectura sobre Anvil:

| Nombre | Tipo IEC | Significado |
|---|---|---|
| `xOnline`              | `BOOL`         | TRUE cuando `eState = Online` o `Degraded`. |
| `eState`               | `eDeviceState` | Estado de fallo actual. |
| `wErrorCount`          | `UDINT`        | Total de errores desde el inicio del puente. |
| `wConsecutiveFailures` | `UDINT`        | Fallos desde el último `Online` (se reinicia en `Online`). |
| `wLastErrorCode`       | `UINT`         | `0` = ninguno; `1..99` comunes; `100+` específicos del protocolo. |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8, rellenado con ceros. |
| `tLastTransition`      | `ULINT`        | Unix time (ms) de la última transición de estado. |

Cuando el dispositivo está vinculado a una **FDD** (descripción de
dispositivo de campo) mediante `catalogRef`, la tabla de estado lista
adicionalmente las extensiones definidas por la FDD, marcadas
`FDD +<offset>` en la columna `Source`.

En código ST cada variable de estado es accesible como
`anvil.<seg>.<dev>.Status.*`:

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## Módulo de bus

Los módulos de bus son rebanadas de E/S dentro de un dispositivo. El
panel muestra:

### Metadatos

  - **Module** (nombre de visualización o `catalogRef`)
  - **Slot** (índice de slot dentro del dispositivo)
  - **Catalog** (referencia FDD, p. ej. `Beckhoff.EL2008`)
  - **Base Addr** (desplazamiento base IEC)

### Tabla de variables IO

Lista cada variable del pool cuyo `busBinding.deviceId` y
`busBinding.moduleSlot` coinciden con este módulo. Columnas:

| Columna | Contenido |
|---|---|
| **Name** | Nombre del pool (editable, p. ej. `Motor_Run`). |
| **Type** | Tipo IEC (editable, p. ej. `BOOL`, `INT`). |
| **Address** | Dirección IEC (`%IX0.0`, solo lectura). |
| **Bus Addr** | Desplazamiento del registro Modbus (solo lectura). |
| **Dir** | `in` o `out` (solo lectura). |

Orden de clasificación: entradas antes que salidas, luego ascendente
por dirección de bus.

## Comportamiento de edición

Cada edición en el panel se ejecuta directamente contra el modelo:

  1. Edición sobre el widget (`editingFinished` / `valueChanged` / `toggled`).
  2. El campo del modelo se actualiza (`seg->name = ...`).
  3. `project->markDirty()` activa la marca de modificado.
  4. Se emite la señal `busConfigEdited`.
  5. La ventana principal refresca la etiqueta del árbol del proyecto si es necesario.

**No** hay un `Apply` explícito ni un `Cancel` — las ediciones surten
efecto de inmediato. `Ctrl+Z` (deshacer) en el árbol del proyecto
revierte la última edición.

## Temas relacionados

  - [Configuración de bus](../bus-config/) — diálogos modales con el
    mismo conjunto de campos, para usuarios avanzados con alto volumen
    de edición.
  - [Panel de variables](../variables/) — el pool que alimenta la
    tabla `IO variables`.
