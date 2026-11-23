#include "stddef.h"
#include "fsm.h"
#include <stdlib.h>
#include "app_driver.h"

struct lb_fsm_t {
	fsm_t fsm;
	int* boton; // puntero porque la ISR y la fsm tienen que acceder a la misma copia de la variable
	int estado_actual_luz;
	int gpio; // no es un puntero si es una constante o una variable interna de la fsm
} ;
typedef struct lb_fsm_t lb_fsm_t;

int lb_fsm_get_luz (fsm_t* this) {
   lb_fsm_t* lb_fsm = (lb_fsm_t*) this;
   int ret = lb_fsm->estado_actual_luz;
   return ret;
}

void lb_fsm_set_luz (fsm_t* this, int value) {
   lb_fsm_t* lb_fsm = (lb_fsm_t*) this;
   lb_fsm->estado_actual_luz = value;
   app_driver_luz_set(lb_fsm->gpio, value);
}

void lb_fsm_toggle_luz (fsm_t* this) {
   lb_fsm_set_luz(this, !(lb_fsm_get_luz(this)));
}


static int comprueba_boton (fsm_t* this) {
	lb_fsm_t* lb_fsm = (lb_fsm_t*) this;
	return *lb_fsm->boton;
}

static void luz_on_and_ack (fsm_t* this) {
	lb_fsm_t* lb_fsm = (lb_fsm_t*) this;
	//app_driver_luz_set(lb_fsm->gpio, 1);
	lb_fsm_set_luz(this, 1);
	*lb_fsm->boton = 0;
}

static void luz_off_and_ack (fsm_t* this) {
	lb_fsm_t* lb_fsm = (lb_fsm_t*) this;
	//app_driver_luz_set(lb_fsm->gpio, 0);
	lb_fsm_set_luz(this, 0);
	*lb_fsm->boton = 0;
}

fsm_t*
fsm_new_led_button(int* boton, int gpio)
{
	static fsm_trans_t tt[] = {
		{ 0, comprueba_boton, 1, luz_on_and_ack },
		{ 1, comprueba_boton, 0, luz_off_and_ack },
		{ -1, NULL, -1, NULL }
	};
	lb_fsm_t* lb_fsm = (lb_fsm_t*) malloc (sizeof (lb_fsm_t)); 
	fsm_init ((fsm_t*) lb_fsm, tt); 
	lb_fsm->boton = boton;
	lb_fsm->gpio = gpio;
	lb_fsm_set_luz((fsm_t*)lb_fsm, 0);
	return (fsm_t*) lb_fsm;
}

