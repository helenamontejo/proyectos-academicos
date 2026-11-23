#ifndef APP_DRIVER_H
#define APP_DRIVER_H

#include "driver/gpio.h"

#define GPIO_OUTPUT_IO_0    18
#define GPIO_OUTPUT_IO_1    19
#define GPIO_OUTPUT_PIN_SEL  (1ULL<<GPIO_OUTPUT_IO_0 | 1ULL<<GPIO_OUTPUT_IO_1)
#define GPIO_INPUT_IO_0     4
#define GPIO_INPUT_PIN_SEL  (1ULL<<GPIO_INPUT_IO_0)
#define ESP_INTR_FLAG_DEFAULT 0

void config_gpios_esp(void);
void app_driver_luz_set(int gpio, int luz);

#endif