#ifndef FSM_BLINK_H
#define FSM_BLINK_H

#include "fsm.h"

fsm_t* fsm_new_blink (int T_med, int gpio); //new

int b_fsm_get_luz (fsm_t* this);
void b_fsm_set_luz (fsm_t* this, int value);
void b_fsm_toggle_luz (fsm_t* this);

#endif
