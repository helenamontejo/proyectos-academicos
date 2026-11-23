#include "stddef.h"
#include "fsm.h"
#include <stdlib.h>
#include "app_driver.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

struct lbt_fsm_t {
	fsm_t fsm;
	int* boton; // puntero porque la ISR y la fsm tienen que acceder a la misma copia de la variable
	TickType_t next;
	int t_ON;
	int gpio;

} ;
typedef struct lbt_fsm_t lbt_fsm_t;

static int comprueba_boton (fsm_t* this) {
	lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
	return *lbt_fsm->boton;
}

static int comprueba_tiempo (fsm_t* this) {
 	lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
 	return xTaskGetTickCount() >= lbt_fsm->next;
}

static int comprueba_boton_and_no_tiempo (fsm_t* this) {
 	lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
 	return *lbt_fsm->boton && !(xTaskGetTickCount() >= lbt_fsm->next);
}

static void luz_on_wait_and_ack (fsm_t* this) {
 lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
 app_driver_luz_set (lbt_fsm->gpio, 1);
 *lbt_fsm->boton = 0;
 lbt_fsm->next = xTaskGetTickCount() + pdMS_TO_TICKS(lbt_fsm->t_ON);
}

static void reset_wait_and_ack (fsm_t* this) {
 lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
 *lbt_fsm->boton = 0;
 lbt_fsm->next = xTaskGetTickCount() + pdMS_TO_TICKS(lbt_fsm->t_ON);
}



// static void luz_on_and_ack (fsm_t* this) {
// 	lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
// 	app_driver_luz_set(lbt_fsm->gpio, 1);
// 	*lbt_fsm->boton = 0;
// }

static void luz_off (fsm_t* this) {
	lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) this;
	app_driver_luz_set(lbt_fsm->gpio, 0);
}

fsm_t*
fsm_new_led_button_temp(int* boton,int t_ON, int gpio)
{
	static fsm_trans_t tt[] = {
		{ 0, comprueba_boton, 1, luz_on_wait_and_ack },
		{ 1, comprueba_tiempo, 0, luz_off },
		{ 1, comprueba_boton_and_no_tiempo, 1, reset_wait_and_ack },
		{ -1, NULL, -1, NULL }
	};
	lbt_fsm_t* lbt_fsm = (lbt_fsm_t*) malloc (sizeof (lbt_fsm_t)); 
	fsm_init ((fsm_t*) lbt_fsm, tt); 
	lbt_fsm->boton = boton;
	lbt_fsm->next = xTaskGetTickCount();
	lbt_fsm->t_ON = t_ON;
	lbt_fsm->gpio = gpio;
	return (fsm_t*) lbt_fsm;
}

