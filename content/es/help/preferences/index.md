---
title: "Preferencias"
summary: "Diálogo central de configuración del editor: Editor, Runtime, PLC, Asistente IA"
---

## Visión general

El **diálogo de Preferencias** es el único punto de entrada para todos
los ajustes globales del editor — todo lo que *no* forma parte del
proyecto abierto sino que configura el editor en sí, la conexión a un
runtime y el comportamiento posterior a la carga.

Abra el diálogo a través de **`Edit > Preferences...`** (algunos temas
lo ubican en `Tools > Preferences...` en su lugar). Pulse **F1**
mientras el diálogo tenga el foco para abrir esta página directamente.

```
Preferences
+-- Editor          (font, tab width, line numbers)
+-- Runtime         (anvild host/port, Anvil debug, network scanner)
+-- PLC             (build mode, auto-start, persist, monitoring)
+-- AI Assistant    (LLM endpoint, tokens, temperature)
```

## Editor

Controla cómo aparece el texto en el editor de código ST y en cualquier
otro campo de entrada de texto.

| Campo | Significado |
|---|---|
| **Fuente**         | Familia de fuente. Prefiltrada a fuentes monoespaciadas (recomendadas: `JetBrains Mono`, `Cascadia Code`, `Consolas`). |
| **Tamaño de fuente**    | Tamaño de fuente en puntos. Predeterminado `10`. |
| **Anchura de tabulación**    | Número de espacios por tabulador. Predeterminado `4`. |
| **Mostrar números de línea** | Muestra números de línea en el margen del editor de código. |

## Runtime

Conexión a un demonio **anvild** y diagnóstico IPC.

| Campo | Significado |
|---|---|
| **Host**         | Hostname o IP del PLC. Predeterminado `localhost`. |
| **Puerto**         | Puerto gRPC de anvild. Predeterminado `50051`. |
| **Usuario**         | Nombre de usuario para autenticación por token. |
| **Anvil Debug**  | Nivel de diagnóstico IPC (`Off`, `Errors only`, `Verbose`). Añade estadísticas adicionales al log de anvild — útil para rastrear desviaciones de tópicos Iceoryx en producción. |

Adicionalmente: **Auto-Connect on start** se conecta automáticamente al
último anvild conectado con éxito al iniciar el editor — práctico en un
portátil de ingeniería dedicado.

El bloque **Network Scanner** en la misma pestaña escanea la LAN en
busca de dispositivos Modbus TCP (puerto 502) y runtimes ForgeIEC
(puerto 50051) e inserta los resultados en la configuración del bus.

## PLC

Controla qué ocurre tras una **carga** al PLC.

| Campo | Significado |
|---|---|
| **Modo de compilación** | `Development` (monitorización en vivo + forzado habilitados) o `Production` (binario reducido, sin puentes de depuración — frontera de seguridad). |
| **Inicio automático del PLC**| Inicia automáticamente el runtime del PLC tras una carga exitosa, omitiendo el diálogo de confirmación. |
| **Persist habilitado** | Habilita la persistencia periódica de variables `VAR_PERSIST`/`RETAIN` en `/var/lib/anvil/persistent.dat`. Los valores sobreviven a un reinicio del runtime. |
| **Intervalo de sondeo Persist** | Segundos entre pasadas de guardado automático (predeterminado `5 s`). |
| **Historial Monitor** | Número de muestras por variable en el grabador del osciloscopio (predeterminado `1000`). |
| **Intervalo Monitor**| Intervalo de muestreo en milisegundos para la monitorización en vivo (predeterminado `100 ms`). |

## Library

Comportamiento de sincronización para la biblioteca estándar entre el
recurso del editor y la ruta de biblioteca del lado del PLC — véase
[Biblioteca](../library/) para el modelo completo de divergencia. Dos
modos:

  - **Auto-Push desactivado** (predeterminado) — al conectarse el
    editor solo registra una nota en el panel de salida cuando se
    detecta divergencia. El push se realiza manualmente mediante
    `Tools > Sync Library`.
  - **Auto-Push activado** — en cada divergencia detectada el editor
    envía automáticamente su versión local de la biblioteca. Útil en
    una configuración con un único programador.

## Asistente IA

Autocompletado de código opcional contra un servidor LLM local
compatible con OpenAI (LM Studio, Ollama, llama.cpp, vLLM).

| Campo | Significado |
|---|---|
| **Habilitar Asistente IA** | Conmuta el autocompletado en línea. |
| **Endpoint API**        | Endpoint compatible con OpenAI, p. ej. `http://localhost:1234/v1`. |
| **Max Tokens**          | Límite de respuesta por solicitud. Predeterminado `2048`. |
| **Temperature**         | `Precise (0.1)`, `Balanced (0.3)`, `Creative (0.7)`, `Wild (1.0)`. |

## Estado UX (autopersistido)

Los siguientes campos se almacenan en segundo plano **sin** pasar por
el diálogo de Preferencias, de modo que el editor se reabre en el
estado exacto en el que lo dejó:

  - Geometría y estado de la ventana (`windowGeometry`, `windowState`)
  - Posiciones de splitter y encabezado (`splitterState`, `headerState`)
  - Altura del panel de salida (`outputPanelHeight`)
  - Último proyecto abierto (`lastProject`) y la lista de archivos recientes
  - Estado de sesión: pestañas POU abiertas, pestaña activa, posición
    de cursor y desplazamiento por POU

## Almacenamiento de ajustes

Los ajustes se almacenan mediante `QSettings` de Qt, específico de la
plataforma:

| Plataforma | Ruta |
|---|---|
| **Windows** | Registro: `HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

Eliminar ese archivo / clave de registro restablece todos los ajustes a
los predeterminados — útil tras una actualización fallida.

## Extensiones planificadas

Backlog (cluster R fase 3): el panel de salida tendrá sus propios
colores de severidad (rojo error, amarillo advertencia, blanco info) y
un tamaño de fuente configurable. Ambas opciones aparecerán entonces
aquí en una nueva pestaña `Output`.

## Temas relacionados

  - [Biblioteca](../library/) — comportamiento de sincronización entre
    editor y runtime.
  - [Configuración de bus](../bus-config/) — ajustes a nivel de
    proyecto que *no* viven aquí sino en el propio segmento /
    dispositivo de bus.
