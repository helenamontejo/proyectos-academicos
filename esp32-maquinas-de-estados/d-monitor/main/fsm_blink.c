#include "stddef.h"
#include "fsm.h"
#include <stdlib.h>
#include "app_driver.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

struct b_fsm_t {
	fsm_t fsm;
	TickType_t next;
   	int T_med;
	int estado_actual_luz;
	int gpio; // no es un puntero si es una constante o una variable interna de la fsm
} ;
typedef struct b_fsm_t b_fsm_t;

int b_fsm_get_luz (fsm_t* this) {
   b_fsm_t* b_fsm = (b_fsm_t*) this;
   int ret = b_fsm->estado_actual_luz;
   return ret;
}

void b_fsm_set_luz (fsm_t* this, int value) {
   b_fsm_t* b_fsm = (b_fsm_t*) this;
   b_fsm->estado_actual_luz = value;
   app_driver_luz_set(b_fsm->gpio, value);
}

void b_fsm_toggle_luz (fsm_t* this) {
   b_fsm_set_luz (this, !(b_fsm_get_luz(this)));
}


static int comprueba_tiempo (fsm_t* this) {
   b_fsm_t* b_fsm = (b_fsm_t*) this;
   return xTaskGetTickCount() >= b_fsm->next;
}

static void luz_toggle_and_wait (fsm_t* this) {
	b_fsm_t* b_fsm = (b_fsm_t*) this;
	//app_driver_luz_set(b_fsm->gpio, (b_fsm->estado_actual_luz = !b_fsm->estado_actual_luz));
	b_fsm_toggle_luz(this);
	b_fsm->next = b_fsm->next + pdMS_TO_TICKS(b_fsm->T_med);
}

fsm_t*
fsm_new_blink (int T_med, int gpio)
{
	static fsm_trans_t tt[] = {
		{ 0, comprueba_tiempo, 0, luz_toggle_and_wait },
		{ -1, NULL, -1, NULL }
	};
	b_fsm_t* b_fsm = (b_fsm_t*) malloc (sizeof (b_fsm_t)); 
	fsm_init ((fsm_t*) b_fsm, tt); 
	b_fsm->next = xTaskGetTickCount();
	b_fsm->T_med = T_med;
	//b_fsm->estado_actual_luz = 0;
	b_fsm->gpio = gpio;
	b_fsm_set_luz((fsm_t*) b_fsm, 0);
	return (fsm_t*) b_fsm;
}

