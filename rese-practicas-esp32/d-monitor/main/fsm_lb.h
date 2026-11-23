#ifndef FSM_LB_H
#define FSM_LB_H

#include "fsm.h"

fsm_t* fsm_new_led_button(int* boton, int gpio); //new

int lb_fsm_get_luz (fsm_t* this);
void lb_fsm_set_luz (fsm_t* this, int value);
void lb_fsm_toggle_luz (fsm_t* this);
#endif
