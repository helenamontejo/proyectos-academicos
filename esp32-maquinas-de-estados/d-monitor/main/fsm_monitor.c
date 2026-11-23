#include "stddef.h"
#include "fsm.h"
#include <stdlib.h>
#include "app_driver.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "fsm_lb.h"
#include "fsm_blink.h"

struct m_fsm_t {
	fsm_t fsm;
	TickType_t next;
	int T;
	fsm_t* fsmLB;
	fsm_t* fsmBLINK;
	int last_luz_lb;
	int last_luz_blink;
} ;
typedef struct m_fsm_t m_fsm_t;

static int comprueba_tiempo_and_cambio_estados (fsm_t* this) {
   m_fsm_t* m_fsm = (m_fsm_t*) this;
   return (xTaskGetTickCount() >= m_fsm->next && !(
               lb_fsm_get_luz(m_fsm->fsmLB) == m_fsm->last_luz_lb &&
               b_fsm_get_luz(m_fsm->fsmBLINK) == m_fsm->last_luz_blink));
}

static int comprueba_tiempo_and_no_cambio_estados (fsm_t* this) {
   m_fsm_t* m_fsm = (m_fsm_t*) this;
   return (xTaskGetTickCount() >= m_fsm->next && 
               lb_fsm_get_luz(m_fsm->fsmLB) == m_fsm->last_luz_lb &&
               b_fsm_get_luz(m_fsm->fsmBLINK) == m_fsm->last_luz_blink);
}

static void reset_estados_wait_and_print (fsm_t* this) {
   m_fsm_t* m_fsm = (m_fsm_t*) this;
   m_fsm->next =  m_fsm->next + pdMS_TO_TICKS(m_fsm->T);
   m_fsm->last_luz_lb = lb_fsm_get_luz(m_fsm->fsmLB);
   m_fsm->last_luz_blink = b_fsm_get_luz(m_fsm->fsmBLINK);
   printf("Luz LED_BUTTON = %d, Luz BLINK = %d\n", m_fsm->last_luz_lb, m_fsm->last_luz_blink);
}

static void reset_wait (fsm_t* this) {
   m_fsm_t* m_fsm = (m_fsm_t*) this;
   m_fsm->next =  m_fsm->next + pdMS_TO_TICKS(m_fsm->T);
}


fsm_t*
fsm_new_monitor (int T, fsm_t* fsmLB, fsm_t* fsmBLINK)
{
	static fsm_trans_t tt[] = {
		{ 0, comprueba_tiempo_and_no_cambio_estados, 0, reset_wait },
		{ 0, comprueba_tiempo_and_cambio_estados, 0, reset_estados_wait_and_print },
		{ -1, NULL, -1, NULL }
	};
	m_fsm_t* m_fsm = (m_fsm_t*) malloc (sizeof (m_fsm_t)); 
	fsm_init ((fsm_t*) m_fsm, tt); 
	m_fsm->next = xTaskGetTickCount();
	m_fsm->T = T;
	m_fsm->fsmLB = fsmLB;
	m_fsm->fsmBLINK = fsmBLINK;
	m_fsm->last_luz_lb = 0;
	m_fsm->last_luz_blink = 0;
	return (fsm_t*) m_fsm;
}

