---
title: "Anvil"
summary: "Sus datos se forjan en nuestro yunque"
---

## El Yunque: Corazon de cada fragua

En cada fragua, el yunque es la pieza central — donde el metal se moldea,
se templa y se refina. **Anvil** es la capa intermedia entre el sistema de
ejecucion del PLC y los bridges de bus de campo. Aqui es donde sus datos
de proceso se forjan: se reciben, se transforman y se distribuyen a los
destinatarios correctos.

Anvil esta construido internamente sobre **IceOryx2** — un framework de
memoria compartida sin copias para comunicacion entre procesos. Sin
serializacion, sin copias, sin compromisos.

---

## Arquitectura

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ Programa PLC │◄───────►│  forgeiecd  │◄───────►│  Bridge Modbus   │──► Dispositivos
│  (Codigo IEC)│  gRPC   │  (Daemon)  │  Anvil  │  Bridge EtherCAT │──► Accionamientos
│              │         │            │ IceOryx2│  Bridge Profibus  │──► Sensores
└──────────────┘         └────────────┘         │  Bridge OPC-UA   │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         Zero-Copy IPC
                         Memoria compartida
```

El intercambio de datos entre `forgeiecd` y los bridges de protocolo se
realiza a traves de **Anvil** — un canal IPC de alto rendimiento basado
en memoria compartida IceOryx2.

---

## Por que Anvil?

### Latencia de microsegundos

Los mecanismos IPC convencionales (pipes, sockets, colas de mensajes) copian
datos entre procesos. Anvil elimina cada copia. Los datos residen en memoria
compartida — el receptor lee directamente.

| Metodo | Latencia tipica | Copias |
|--------|----------------|--------|
| Socket TCP | 50–200 us | 2–4 |
| Socket Unix | 10–50 us | 2 |
| **Anvil (IceOryx2)** | **< 1 us** | **0** |

### Calidad industrial

- Comportamiento determinista — sin asignacion dinamica de memoria en la ruta critica
- Algoritmos sin bloqueo — sin bloqueos, sin deadlocks
- Modelo publish/subscribe — acoplamiento debil entre productor y consumidor
- Gestion automatica del ciclo de vida — los bridges se supervisan y reinician automaticamente

### PUBLISH/SUBSCRIBE en el programa IEC

```iec
VAR_GLOBAL PUBLISH 'Motores'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensores'
    Temperatura AT %IW0   : INT;
    Presion     AT %IW2   : INT;
END_VAR
```

---

## Protocolos soportados

| Protocolo | Bridge | Estado |
|-----------|--------|--------|
| **Modbus TCP** | `forgeiec-modbustcp` | Disponible |
| **Modbus RTU** | `forgeiec-modbusrtu` | Disponible |
| **EtherCAT** | `forgeiec-ethercat` | En desarrollo |
| **Profibus DP** | `forgeiec-profibus` | En desarrollo |
| **OPC-UA** | `forgeiec-opcua` | Planificado |

Cada bridge funciona como un proceso independiente. `forgeiecd` inicia,
supervisa y reinicia los bridges automaticamente.

---

<div style="text-align:center; padding: 2rem;">

**Anvil — Donde los datos se forjan en comandos de control.**

blacksmith@forgeiec.io

</div>
