---
title: "Segmentos de bus"
summary: "Configuración de un segmento de bus de campo (una red física en una interfaz)"
---

## Visión general

Un **segmento de bus** describe **una red física en una interfaz del
controlador PLC** — típicamente un puerto Ethernet (`eth0`, `enp3s0`)
para Modbus TCP / EtherCAT / EtherNet-IP, o un puerto serie
(`/dev/ttyUSB0`) para Modbus RTU / Profibus DP. Para cada segmento, el
demonio `anvild` lanza **exactamente un proceso puente**
(`tongs-modbustcp`, `tongs-ethercat`, ...) que gestiona el tráfico
hacia todos los dispositivos de ese segmento.

Un proyecto puede contener cualquier número de segmentos — cada uno con
su propio protocolo, su propia interfaz y su propia cadencia de sondeo.
Por ejemplo, un controlador de eje EtherCAT rápido (`eth1`, 1 ms) y un
sondeador lento de sensores Modbus TCP (`eth0`, 100 ms) pueden ejecutarse
en paralelo en el mismo proyecto.

## Campos de un segmento

La definición de la estructura reside en
`editor/include/model/FBusSegmentConfig.h`. Un segmento se persiste en
el proyecto `.forge` como `<fi:segment>` dentro de `<fi:busConfig>`
(véase [Configuración de bus](../)).

### Identidad + protocolo

| Campo | Tipo | Significado |
|---|---|---|
| `segmentId` | UUID | Clave primaria estable — generada automáticamente al crear, no editable. Sobrevive al cambio de nombre, cambio de protocolo y cambio de IP. |
| `protocol` | enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Determina qué demonio puente se inicia. |
| `name` | string | Etiqueta de usuario (p. ej. `"Bus de campo nave 1"`). Texto libre, mostrado en el árbol y en los registros. |
| `enabled` | bool | Interruptor de encendido/apagado. `false` = el puente no se inicia, los dispositivos permanecen offline. Predeterminado: `true`. |

### Interfaz + enrutamiento

| Campo | Tipo | Significado |
|---|---|---|
| `interface` | string | Interfaz de red (`eth0`, `enp3s0`, `/dev/ttyUSB0`). El puente la pasa a la API de socket / serie. |
| `bindAddress` | string (IP/CIDR) | IP de origen para conexiones TCP salientes, p. ej. `192.168.24.100/24`. Vacío = el SO elige la primera IP de la interfaz. |
| `gateway` | string (IP) | Pasarela predeterminada para los paquetes que salen de la subred local. Vacío = sin pasarela. |
| `pollIntervalMs` | int (ms) | Intervalo de sondeo del puente. `0` = lo más rápido posible (bucle activo / tiempo real). Típico: `100` para Modbus TCP, `0` para EtherCAT. |

### Configuración de red (avanzada)

Estos campos se añadieron en el sprint de configuración de red y cubren
casos en los que los valores predeterminados del SO no son suficientes
— típicamente: muchas conexiones TCP paralelas por esclavo, sesiones
TCP de larga duración a través de NAT, o varias subredes en una única
NIC.

| Campo | Tipo | Significado |
|---|---|---|
| `subnetCidr` | string (CIDR) | Subred local del segmento, p. ej. `192.168.24.0/24`. Permite al puente enrutar correctamente las anulaciones de pasarela por dispositivo cuando la NIC vinculada lleva varias redes. |
| `sourcePortRange` | string `"min-max"` | Pool de puertos TCP de origen para conexiones salientes, p. ej. `30000-39999`. Vacío = el SO elige del rango efímero. Importante cuando se necesitan muchas conexiones paralelas al mismo esclavo (una conexión por puerto de origen). |
| `keepAliveIdleSec` | int (s) | Segundos de inactividad antes de enviar la primera sonda de keep-alive TCP. `0` = predeterminado del SO. |
| `keepAliveIntervalSec` | int (s) | Espaciado entre sondas de keep-alive. `0` = predeterminado del SO. |
| `keepAliveCount` | int | Número de sondas fallidas antes de declarar la conexión muerta. `0` = predeterminado del SO. |
| `maxConnections` | int | Límite superior del pool de conexiones. `0` = ilimitado. Útil contra esclavos con un límite de conexión estricto. |
| `vlanId` | int (1..4094) | Etiqueta VLAN 802.1Q para tramas salientes. `0` = sin etiqueta. |

### Configuración específica del protocolo

El mapa `settings` (clave/valor) contiene todos los valores que solo
tienen sentido para un protocolo específico — p. ej. para Modbus TCP:
`port`, `timeout_ms`; para Modbus RTU: `serial_port`, `baud_rate`,
`parity`, `stop_bits`; para Profibus: `master_address`. `log_level` y
`log_file` también se mantienen agnósticos al protocolo en este mismo
mapa.

## Flujo de edición

En el panel del árbol del bus ambos caminos son equivalentes — operan
sobre el mismo conjunto de campos y tienen el mismo efecto semántico:

| Acción | Efecto |
|---|---|
| **Clic simple** sobre un nodo de segmento | El `FPropertiesPanel` (acoplamiento predeterminado: lado derecho) muestra todos los campos como editores en línea — los cambios se escriben al proyecto en `editingFinished` y marcan el proyecto como modificado. |
| **Doble clic** sobre un nodo de segmento | Abre el `FSegmentDialog` modal con el mismo conjunto de campos, agrupados en *General* / *Modbus TCP* / *Advanced Network* / *Logging*. OK confirma, Cancel descarta. |

## Ejemplo: segmento Modbus TCP

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

Este segmento inicia `tongs-modbustcp` en `eth0` con IP de origen
`192.168.24.100`, sondea todos los dispositivos cada 100 ms y acepta
hasta 2000 ms de tiempo de respuesta por solicitud antes de emitir un
error de timeout en el flujo de estado.

## Temas relacionados

* [Configuración de bus — visión general del esquema](../) —
  persistencia XML y mecanismo PLCopen `<addData>`.
* [Dispositivos de bus](../devices/) — dispositivos dentro de un segmento.
* [Formato de archivo de proyecto](../../file-format/) — la raíz XML
  `.forge`.
