---
title: "Anvil"
description: "Runtime PLC en tiempo real con IPC Zero-Copy"
weight: 2
---

## Anvil -- El runtime en el corazon de la forja

En toda forja, el yunque es la pieza central -- donde el metal se forma,
se templa y se refina. **Anvil** es la capa intermedia entre el runtime
del PLC y los bridges de protocolo. Aqui es donde sus datos de proceso
se forjan: recibidos, transformados y distribuidos a los destinatarios
correctos.

Anvil utiliza una capa de transporte propietaria de memoria compartida
Zero-Copy para la comunicacion entre procesos. Sin serializacion,
sin copias, sin compromisos.

---

## Arquitectura

```
+--------------+         +------------+         +------------------+
|              |         |            |         |                  |
| Programa     |<------->|  anvild    |<------->|  Modbus Bridge   |---> Dispositivos
|  PLC         |  gRPC   |  (Daemon)  |  Anvil  |  EtherCAT Bridge |---> Accionamientos
|  (Codigo IEC)|         |            |         |  Profibus Bridge |---> Sensores
+--------------+         +------------+         |  OPC-UA Bridge   |---> SCADA
                                                +------------------+

                         <--- Anvil --->
                         Zero-Copy IPC
                         Memoria compartida
```

El intercambio de datos entre `anvild` y los bridges de protocolo se realiza
a traves de **Anvil** -- un canal IPC de alto rendimiento basado en memoria
compartida Zero-Copy. Cada segmento recibe su propio canal de comunicacion.

---

## Por que Anvil?

### Latencia en microsegundos

Los mecanismos IPC convencionales (pipes, sockets, colas de mensajes) copian
datos entre procesos. Anvil elimina cada copia. Los datos residen en memoria
compartida -- el receptor lee directamente.

| Metodo | Latencia tipica | Copias |
|--------|----------------|--------|
| TCP Socket | 50-200 us | 2-4 |
| Unix Socket | 10-50 us | 2 |
| **Anvil** | **< 1 us** | **0** |

### Calidad industrial

- Comportamiento determinista -- sin asignacion de memoria dinamica en la ruta critica
- Algoritmos sin bloqueo -- sin bloqueos, sin deadlocks
- Modelo Publish/Subscribe -- acoplamiento debil entre productor y consumidor
- Gestion automatica del ciclo de vida -- los bridges se supervisan y reinician en caso de fallo

### PUBLISH/SUBSCRIBE en el programa IEC

Anvil se integra de forma transparente en la programacion IEC 61131-3:

```iec
VAR_GLOBAL PUBLISH 'Motores'
    K1_Red      AT %QX0.0 : BOOL;
    K1_Velocidad AT %QW10 : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensores'
    Temperatura AT %IW0   : INT;
    Presion     AT %IW2   : INT;
END_VAR
```

Las palabras clave PUBLISH/SUBSCRIBE son una extension ForgeIEC del estandar
IEC 61131-3. El compilador genera automaticamente los enlaces Anvil.

---

## Protocolos soportados

| Protocolo | Bridge | Estado |
|-----------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | Disponible |
| **Modbus RTU** | `tongs-modbusrtu` | Disponible |
| **EtherCAT** | `tongs-ethercat` | En desarrollo |
| **Profibus DP** | `tongs-profibus` | En desarrollo |
| **OPC-UA** | `tongs-opcua` | Planificado |

Cada bridge funciona como un proceso independiente. `anvild` inicia,
supervisa y reinicia los bridges automaticamente. Un fallo de un bridge
no afecta ni al PLC ni a los demas bridges.

---

## Detalles tecnicos

- **Framework IPC**: Anvil (memoria compartida Zero-Copy propietaria)
- **Arquitectura**: Un canal publisher/subscriber por segmento de bus
- **Formato de datos**: Variables IEC crudas -- sin serializacion, sin overhead
- **Plataformas**: x86_64, ARM64, ARMv7 (Linux)
- **Modelo de procesos**: Un proceso bridge por segmento activo

---

<div style="text-align:center; padding: 2rem;">

**Anvil -- Donde los datos se forjan en comandos de control.**

blacksmith@forgeiec.io

</div>
