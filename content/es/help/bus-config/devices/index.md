---
title: "Dispositivos de bus"
summary: "Configuración de un dispositivo dentro de un segmento de bus (esclavo Modbus, esclavo EtherCAT, ...)"
---

## Visión general

Un **dispositivo de bus** es un **único dispositivo dentro de un
segmento** — típicamente un esclavo Modbus TCP (bloque de E/S, variador),
un esclavo EtherCAT (eje servo, acoplador de E/S), un esclavo Profibus
DP o un adaptador EtherNet-IP. Para cada dispositivo, el puente
responsable mantiene una conexión lógica, sondea los registros
configurados y publica los datos a través del grupo Anvil IPC al
runtime del PLC.

Un dispositivo puede ser **modular**: un acoplador de bus (slot 0)
lleva 1..N módulos de E/S en los slots 1..N. Los dispositivos compactos
sin slots de expansión tienen una lista `modules` vacía — las variables
viven entonces directamente en el slot 0.

## Campos de un dispositivo

La definición de la estructura reside en
`editor/include/model/FBusSegmentConfig.h` (junto al segmento). Un
dispositivo se persiste en el proyecto `.forge` como `<fi:device>`
dentro de `<fi:segment>` (véase [Configuración de bus](../)).

### Identidad + direccionamiento

| Campo | Tipo | Significado |
|---|---|---|
| `deviceId` | UUID | Clave primaria estable — generada automáticamente al crear. Sobrevive al cambio de hostname y de IP, manteniendo estables todas las vinculaciones de variables. |
| `hostname` | string | Etiqueta visible para el usuario (`"Maibeere"`, `"Stachelbeere"`). Compatible con DHCP, pero explícitamente **no** la clave primaria. |
| `ipAddress` | string (IP) | Dirección IP (Modbus TCP / EtherNet-IP). Vacío para dispositivos sin IP (los esclavos EtherCAT se identifican mediante su posición en el bus). |
| `port` | int | Puerto TCP. Predeterminado `502` (Modbus TCP). |
| `slaveId` | int | ID de esclavo Modbus (1..247). Habitualmente `1` sobre TCP. |
| `anvilGroup` | string | Grupo Anvil IPC para transporte sin copia entre el puente y el runtime del PLC. Convención: el mismo nombre que `hostname`. |
| `catalogRef` | string | Referencia opcional a una entrada de catálogo FDD (`"WAGO-750-352"`) que describe el dispositivo. |
| `description` | string | Descripción de texto libre (`"Bewaesserungsventil Sued"`). |

### Módulos (slots)

| Campo | Tipo | Significado |
|---|---|---|
| `modules` | lista de `FBusModuleConfig` | Módulos de E/S del dispositivo. Slot 0 = acoplador / dispositivo compacto, slots 1..N = módulos de expansión. Por módulo: `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

### Anulaciones por dispositivo

Estos campos sobrescriben — solo para **este** dispositivo — los
valores correspondientes del segmento. `0` o cadena vacía significa
*heredar del segmento*. En el panel de propiedades se ubican bajo el
bloque *Advanced Overrides*, normalmente plegado.

| Campo | Tipo | Significado |
|---|---|---|
| `mac` | string `AA:BB:CC:DD:EE:FF` | Dirección MAC para verificación ARP estática / identidad. Protege contra el robo de IP en dispositivos DHCP. |
| `endianness` | enum | Orden de palabra/byte para valores multi-registro: `"ABCD"` (big-endian, predeterminado IEC), `"DCBA"` (intercambio de palabras), `"BADC"` (intercambio de bytes), `"CDAB"` (intercambio de bytes + palabras). Vacío = heredar del segmento. |
| `timeoutOverrideMs` | int (ms) | Timeout por dispositivo. `0` = usar el timeout del segmento. |
| `retryCount` | int | Número de reintentos por solicitud. `0` = predeterminado del segmento. |
| `connectionMode` | enum | `"always"` (mantener TCP abierto entre ciclos) o `"on_demand"` (reconectar por transacción). Vacío = predeterminado del segmento / puente. |
| `gatewayOverride` | string (IP) | Pasarela por dispositivo cuando el dispositivo se encuentra en una subred diferente a la NIC vinculada. |

### Configuración específica del dispositivo

El mapa `settings` (clave/valor) lleva valores que solo tienen sentido
para este dispositivo o su tipo de dispositivo — p. ej. un umbral de
un variador o un código de función preferido.

## Flujo de edición

| Acción | Efecto |
|---|---|
| **Clic simple** sobre un nodo de dispositivo | `FPropertiesPanel` muestra todos los campos como editores en línea — bloque General (hostname, IP, puerto, ID de esclavo, grupo Anvil), bloque de anulación (MAC, timeout, reintentos, endianness, modo de conexión, anulación de pasarela, descripción) y la tabla de estado. |
| **Doble clic** sobre un nodo de dispositivo | Abre el `FBusDeviceDialog` modal con el mismo conjunto de campos. En modo edición el botón "Import from catalog" está bloqueado para que una importación FDD posterior no pueda sobrescribir silenciosamente las vinculaciones de variables de E/S existentes. |

## Variables de estado (solo lectura)

En tiempo de ejecución cada dispositivo publica una estructura de
estado que el demonio envía a través del flujo de estado gRPC. Estos
valores se muestran en el panel de propiedades como una **tabla de
solo lectura** y **no son editables** desde la UI — los escribe el
puente. Desde el código ST siguen siendo direccionables como rutas
cualificadas bajo `anvil.<seg>.<dev>.Status.*`:

| Variable de estado | Tipo | Significado |
|---|---|---|
| `xOnline` | `BOOL` | Dispositivo actualmente accesible (la última solicitud fue respondida). |
| `eState` | `INT` | Enum de estado: 0=offline, 1=conectando, 2=online, 3=error. |
| `wErrorCount` | `WORD` | Contador de solicitudes fallidas desde el inicio del puente. |
| `sLastErrorMsg` | `STRING` | Último mensaje de error (timeout, excepción Modbus, ...). |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## Ejemplo: acoplador de bus WAGO 750 con dos slots

Un acoplador de bus Modbus TCP 750-352 con un módulo 8-DI (750-430) en
el slot 1 y un módulo 8-DO (750-530) en el slot 2:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

Las 8 entradas aparecen en el pool de direcciones como
`%IX0.0..%IX0.7` con `deviceId="0e5d5537-..."`, `moduleSlot=1` y
`modbusAddress=0..7`. Las 8 salidas igualmente con `moduleSlot=2`.

## Temas relacionados

* [Segmentos de bus](../segments/) — la red en la que vive el dispositivo.
* [Configuración de bus — visión general del esquema](../) —
  persistencia XML.
* [Formato de archivo de proyecto](../../file-format/) — pool de
  direcciones y vinculaciones variable-dispositivo.
