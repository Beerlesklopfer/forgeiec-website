---
title: "Configuracion de Bus"
summary: "Esquema XML PLCopen para la configuracion de buses de campo industriales"
---

## Namespace

```
https://forgeiec.io/v2/bus-config
```

Este esquema describe la extension ForgeIEC del formato XML PLCopen
para almacenar la configuracion de buses de campo dentro de archivos
de proyecto `.forge`. Utiliza el mecanismo estandar `<addData>`
definido por PLCopen TC6.

## Resumen

La configuracion de bus define la topologia fisica de una planta:
los **segmentos** (redes de bus) contienen **dispositivos**, y cada
dispositivo esta vinculado a las variables de E/S del proyecto
mediante un bus binding.

```
Proyecto .forge
  +-- Segmentos (redes de bus)
  |     +-- Dispositivos
  |           +-- Variables (via bus binding en el pool de direcciones)
  +-- Pool de direcciones (FAddressPool)
        +-- Variable: DI_1, %IX0.0, busBinding -> Maibeere
        +-- Variable: DO_1, %QX0.0, busBinding -> Maibeere
```

## Estructura XML

La configuracion de bus se almacena como `<addData>` a nivel de proyecto:

```xml
<project>
  <!-- Contenido PLCopen estandar -->
  <types>...</types>
  <instances>...</instances>

  <!-- Configuracion de bus ForgeIEC -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Bus de campo Nave 1"
                    enabled="true"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    gateway=""
                    pollIntervalMs="0">

          <fi:device hostname="Maibeere"
                     ipAddress="192.168.24.25"
                     port="502"
                     slaveId="1"
                     anvilGroup="Maibeere"/>

          <fi:device hostname="Stachelbeere"
                     ipAddress="192.168.24.26"
                     port="502"
                     slaveId="1"
                     anvilGroup="Stachelbeere"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

## Elementos

### `fi:busConfig`

Elemento raiz. Contiene uno o mas elementos `fi:segment`.

| Atributo | Requerido | Descripcion |
|----------|-----------|-------------|
| `xmlns:fi` | si | Namespace: `https://forgeiec.io/v2` |

### `fi:segment`

Un segmento de bus de campo (red fisica).

| Atributo | Requerido | Tipo | Descripcion |
|----------|-----------|------|-------------|
| `id` | si | UUID | Identificador unico del segmento |
| `protocol` | si | String | Protocolo: `modbustcp`, `modbusrtu`, `ethercat`, `profibus` |
| `name` | si | String | Nombre visible (libre) |
| `enabled` | no | Bool | Segmento activo (`true`) o desactivado (`false`). Por defecto: `true` |
| `interface` | no | String | Interfaz de red (ej. `eth0`, `/dev/ttyUSB0`) |
| `bindAddress` | no | String | IP/CIDR de la interfaz (ej. `192.168.24.100/24`) |
| `gateway` | no | String | Direccion de gateway (vacio = sin gateway) |
| `pollIntervalMs` | no | Int | Intervalo de sondeo en milisegundos (`0` = lo mas rapido posible) |

### `fi:device`

Un dispositivo dentro de un segmento.

| Atributo | Requerido | Tipo | Descripcion |
|----------|-----------|------|-------------|
| `hostname` | si | String | Nombre del dispositivo (usado como ID) |
| `ipAddress` | no | String | Direccion IP (Modbus TCP) |
| `port` | no | Int | Puerto TCP (por defecto: `502`) |
| `slaveId` | no | Int | ID esclavo Modbus |
| `anvilGroup` | no | String | Grupo Anvil IPC para transporte zero-copy |

## Vinculacion Variable-Dispositivo

Las variables de E/S **no** se listan dentro del elemento `fi:device`.
En su lugar, cada variable del pool de direcciones lleva un atributo
`busBinding` que apunta al `hostname` del dispositivo:

```
FLocatedVariable
  name: "DI_1"
  address: "%IX0.0"
  anvilGroup: "Maibeere"
  busBinding:
    deviceId: "Maibeere"
    modbusAddress: 0
    count: 1
```

## Asignacion de direcciones IEC

La direccion IEC de una variable vinculada se deriva de la topologia fisica:

```
Base del segmento + Offset del dispositivo + Posicion del registro
```

| Rango de direcciones | Significado | Fuente |
|----------------------|-------------|--------|
| `%IX` / `%IW` / `%ID` | Entrada fisica | Bus binding |
| `%QX` / `%QW` / `%QD` | Salida fisica | Bus binding |
| `%MX` / `%MW` / `%MD` | Marcador (sin E/S fisica) | Asignador de pool |

## Protocolos soportados

| Protocolo | Valor `protocol` | Medio | Daemon bridge |
|-----------|-----------------|-------|---------------|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485 (serie) | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | Ethernet (tiempo real) | `tongs-ethercat` |
| Profibus DP | `profibus` | Serie (bus de campo) | `tongs-profibus` |

## Compatibilidad

El atributo `handleUnknown="discard"` asegura que las herramientas
PLCopen que no conocen ForgeIEC puedan ignorar la configuracion de bus
sin generar errores. A su vez, ForgeIEC lee los bloques `<addData>`
desconocidos de otros fabricantes y los preserva al guardar.

---

<div style="text-align:center; padding: 2rem;">

**Configuracion de Bus ForgeIEC — Sin conexion, conforme PLCopen, sin redundancia.**

blacksmith@forgeiec.io

</div>
