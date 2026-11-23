#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "app_driver.h"
#include "fsm_blink.h"
#include "fsm_lb.h"
#include "fsm_monitor.h"

static int boton;


static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    const int antirrebotes_ms = 250;
    static TickType_t next_antirrebotes = 0;
    if (xTaskGetTickCount() >= next_antirrebotes) {
        boton = 1;
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
    //gpio_isr_handler_add(GPIO_INPUT_IO_1, gpio_isr_handler1, (void*) GPIO_INPUT_IO_1);
}

void app_main(void)
{
    config_gpios_esp();
    config_ISR();
    
    fsm_t* fsmLB = fsm_new_led_button(&boton, GPIO_OUTPUT_IO_0); // Asumo Tlb=500ms suficiente para menos frames
    fsm_t* fsmBLINK = fsm_new_blink(5000, GPIO_OUTPUT_IO_1); // Tblink=10s Tblink_med=5s
    fsm_t* fsmMON = fsm_new_monitor(500, fsmLB, fsmBLINK);
    
	TickType_t next = xTaskGetTickCount();
	while (1) {
		static int frame = 0;
        switch (frame)
        {
        case 0:
            fsm_fire (fsmLB);
            fsm_fire (fsmMON);
		    fsm_fire (fsmBLINK);
            break;
        
        default:
            fsm_fire (fsmLB);
            fsm_fire (fsmMON);
            break;
        }
		frame = (frame + 1) % 10;
        vTaskDelayUntil(&next, pdMS_TO_TICKS(500)); // Ts = 500 ms
	}
}
