# Prácticas de sistemas empotrados con ESP32

Prácticas de la asignatura RESE, realizadas en abril de 2026 en pareja por Helena Montejo y Flavia Buitrón. Están escritas en C con ESP-IDF y FreeRTOS para un ESP32. Cada práctica modela el comportamiento del sistema con máquinas de estados finitas (FSM).

## Prácticas

| Carpeta | Qué hace |
|---|---|
| `a-led-button` | Un LED que se controla con un botón, con una FSM. |
| `a-led-button-pfd` | La misma práctica, planteada a partir de un diagrama de flujo de proceso (PFD). |
| `b-led-button` | LED y botón con un temporizador. |
| `c-blink` | Parpadeo del LED con una FSM. |
| `c-extra-led-button-blink` | Combina el botón y el parpadeo con dos FSM. |
| `d-monitor` | Una FSM monitor que supervisa el estado del botón y del parpadeo. Es la más completa. |

## Estructura
Cada carpeta es un proyecto de ESP-IDF: `main/` contiene el código (`app_driver` para el hardware, `fsm` como base de las máquinas de estados y un `fsm_*` por cada FSM) y `CMakeLists.txt` la configuración de compilación.

## Compilar
Con ESP-IDF instalado, dentro de una carpeta:

    idf.py build
    idf.py flash monitor

Los pines usados están en `main/app_driver.h`: salidas GPIO 18 y 19, y entrada GPIO 4 (botón).

## Notas
Las carpetas `build/` y los ficheros `sdkconfig` no se incluyen, porque se generan al compilar.
