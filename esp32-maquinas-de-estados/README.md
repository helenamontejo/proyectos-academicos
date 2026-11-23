# Máquinas de estados con ESP32

Prácticas de la asignatura RESE, realizadas en abril de 2026 en pareja por Helena Montejo y Flavia Buitrón. Están escritas en C con ESP-IDF y FreeRTOS para un ESP32. Cada práctica modela el comportamiento del sistema con máquinas de estados finitas (FSM).

## Prácticas

| Carpeta | Qué hace |
|---|---|
| `a-led-button` | Una FSM que controla un LED con un botón. |
| `a-led-button-2fsm` | Dos FSM de LED y botón, una por LED (GPIO 18 y 19), ejecutadas desde el mismo bucle. |
| `a-led-button-pfd` | Dos FSM de LED y botón, cada una en su propia tarea de FreeRTOS con distinta prioridad. |
| `b-led-button` | LED y botón con temporizador (3 s). |
| `b-led-button-temp-2fsm` | Dos FSM de LED, botón y temporizador, con 3 s y 6 s. |
| `c-blink` | Parpadeo de un LED con una FSM (3 s). |
| `extra-blink-2fsm` | Dos FSM de parpadeo, con periodos de 3 s y 1,5 s. |
| `c-extra-led-button-blink` | Una FSM de LED y botón, y otra de parpadeo (5 s), en dos LED. |
| `extra-led-button-blink-temp` | Tres FSM: LED y botón, LED y botón con temporizador (15 s) y parpadeo (1,5 s), en tres LED. |
| `d-monitor` | Una FSM monitor que supervisa el estado de la FSM de LED y botón y de la de parpadeo. Es la más completa. |

## Estructura
Cada carpeta es un proyecto de ESP-IDF: `main/` contiene el código (`app_driver` para el hardware, `fsm` como base de las máquinas de estados y un `fsm_*` por cada FSM) y `CMakeLists.txt` la configuración de compilación.

## Compilar
Con ESP-IDF instalado, dentro de una carpeta:

    idf.py build
    idf.py flash monitor

Los pines están definidos en `main/app_driver.h` de cada proyecto.

## Notas
Las carpetas `build/` y los ficheros `sdkconfig` no se incluyen, porque se generan al compilar.
