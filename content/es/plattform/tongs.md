---
title: "Tongs"
description: "Bridges Fieldbus -- Modbus, EtherCAT, Profibus"
weight: 6
---

## Tongs -- Bridges Fieldbus

Las tenazas son la herramienta del forjador para agarrar el metal al rojo
vivo. **Tongs** agarra los datos de los dispositivos de campo y los
transporta al runtime del PLC. Cada protocolo de bus de campo dispone de su
propia bridge, gestionada como un proceso independiente.

---

## Protocolos soportados

### Modbus TCP

Comunicacion Ethernet para dispositivos Modbus. Lectura y escritura de
registros, bobinas y entradas discretas. Escaner de red integrado para la
deteccion automatica de dispositivos.

| Propiedad | Valor |
|-----------|-------|
| Transporte | TCP/IP (Ethernet) |
| Bridge | `tongs-modbustcp` |
| Funciones | FC1, FC2, FC3, FC4, FC5, FC6, FC15, FC16 |
| Estado | Disponible |

### Modbus RTU

Comunicacion serie para dispositivos Modbus sobre RS-485. Mismas funciones
que Modbus TCP, adaptadas al transporte serie.

| Propiedad | Valor |
|-----------|-------|
| Transporte | Serie RS-485 |
| Bridge | `tongs-modbusrtu` |
| Estado | Disponible |

### EtherCAT

Bus de campo Ethernet en tiempo real para accionamientos, servomotores y
modulos de E/S de alto rendimiento.

| Propiedad | Valor |
|-----------|-------|
| Transporte | Ethernet (tiempo real) |
| Bridge | `tongs-ethercat` |
| Estado | En desarrollo |

### Profibus DP

Estandar industrial probado para la comunicacion con dispositivos de campo
en instalaciones existentes.

| Propiedad | Valor |
|-----------|-------|
| Transporte | RS-485 / Fibra optica |
| Bridge | `tongs-profibus` |
| Estado | En desarrollo |

---

## Arquitectura

Cada bridge funciona como un proceso independiente, gestionado por el daemon
`anvild`. La comunicacion con el runtime se realiza mediante Anvil (Zero-Copy
IPC). Un fallo de un bridge no afecta ni al PLC ni a los demas bridges.

```
anvild
  |
  +-- tongs-modbustcp --segment mb1 --> Dispositivos Modbus TCP
  |
  +-- tongs-modbusrtu --segment mb2 --> Dispositivos Modbus RTU
  |
  +-- tongs-ethercat  --segment ec1 --> Dispositivos EtherCAT
  |
  +-- tongs-profibus  --segment pb1 --> Dispositivos Profibus
```

### Gestion de procesos

- Arranque automatico de los bridges al iniciar el runtime
- Supervision continua -- reinicio en caso de fallo
- Un proceso por segmento de bus activo
- Registro independiente por bridge

---

## Configuracion

Los segmentos de bus se configuran en `config.toml` en el sistema objetivo.
Cada segmento define el protocolo, la interfaz de red y los dispositivos
conectados.

### Variables de E/S

Cada dispositivo expone variables de entrada y de salida:

- **Direccion "in"** -- Lectura desde el dispositivo (Subscribe)
- **Direccion "out"** -- Escritura hacia el dispositivo (Publish)
- Asignacion automatica de direcciones IEC (%I, %Q) sin conflictos

---

<div style="text-align:center; padding: 2rem;">

**Tongs -- Las tenazas que agarran sus datos de campo.**

blacksmith@forgeiec.io

</div>
