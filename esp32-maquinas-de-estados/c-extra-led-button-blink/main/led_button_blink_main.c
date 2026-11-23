#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "app_driver.h"
#include "fsm_lb.h"
#include "fsm_blink.h"
#include "esp_timer.h"

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
    
    fsm_t* fsmLB = fsm_new_led_button(&boton, GPIO_OUTPUT_IO_0);
    fsm_t*fsmBLINK_10s= fsm_new_blink(5000, GPIO_OUTPUT_IO_1);
	TickType_t next = xTaskGetTickCount();
    // uint64_t init_time;
    // uint64_t end_time;
    // uint64_t tiempo_ejecucion=0;
    // while (1) {
    //     init_time=esp_timer_get_time();
    //     fsm_fire (fsmLB);
    //     end_time=esp_timer_get_time();
    //     if(end_time-init_time>tiempo_ejecucion){
    //         tiempo_ejecucion=end_time-init_time;
    //         printf("Tiempo de ejecucion max C: %llu us\n", tiempo_ejecucion);
    //     }
    //     vTaskDelayUntil(&next, pdMS_TO_TICKS(100)); //100ms de espera
    // }
	while (1) {
        static int frame=0;
        switch (frame)
        {
        case 0:
            fsm_fire (fsmLB);
            fsm_fire(fsmBLINK_10s);
            break;
        
        default:
            fsm_fire (fsmLB);
            break;
        }
		frame= (frame + 1) % 10
		vTaskDelayUntil(&next, pdMS_TO_TICKS(500)); // itera cada 100 ms
	}

}
