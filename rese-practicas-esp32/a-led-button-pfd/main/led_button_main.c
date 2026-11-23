#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "app_driver.h"
#include "fsm_lb.h"
#include "esp_timer.h"

static int boton;
static int boton1;

static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    const int antirrebotes_ms = 250;
    static TickType_t next_antirrebotes = 0;
    if (xTaskGetTickCount() >= next_antirrebotes) {
        boton = 1;
        next_antirrebotes = xTaskGetTickCount() + pdMS_TO_TICKS(antirrebotes_ms);
    }
}

static void IRAM_ATTR gpio_isr_handler1(void* arg)
{
    const int antirrebotes_ms = 250;
    static TickType_t next_antirrebotes = 0;
    if (xTaskGetTickCount() >= next_antirrebotes) {
        boton1 = 1;
        next_antirrebotes = xTaskGetTickCount() + pdMS_TO_TICKS(antirrebotes_ms);
    }
}

static void config_ISR(void)
{
    //install gpio isr service
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    //hook isr handler for specific gpio pin
    gpio_isr_handler_add(GPIO_INPUT_IO_0, gpio_isr_handler, (void*) GPIO_INPUT_IO_0);
    //hook isr handler for specific gpio pin
    gpio_isr_handler_add(GPIO_INPUT_IO_1, gpio_isr_handler1, (void*) GPIO_INPUT_IO_1);
}

static void lb_thread (void* pvParameters)
{
    fsm_t* fsmLB = (fsm_t*) pvParameters;
    TickType_t next = xTaskGetTickCount();
    while (1) {
        fsm_fire (fsmLB);
        vTaskDelayUntil(&next, pdMS_TO_TICKS(300)); //Periodo tarea lb 300ms
    }
}

void app_main(void)
{
    config_gpios_esp();
    config_ISR();
    
    fsm_t* fsmLB = fsm_new_led_button(&boton, GPIO_OUTPUT_IO_0);
    fsm_t* fsmLB1 = fsm_new_led_button(&boton1, GPIO_OUTPUT_IO_1);
    TaskHandle_t task1, task2;
    // Si hay más de una tarea
    // TaskHandle_t task1, task2, task3;
    xTaskCreate(lb_thread, "lb_thread", 4096, (void*) fsmLB, 2, &task1);
    xTaskCreate(lb_thread, "lb_thread1", 4096, (void*) fsmLB1, 1, &task2);
    //xTaskCreate(fsm3, "fsm3", 4096, NULL, 3, &task3);
}
