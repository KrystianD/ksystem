/* ----------------------- Platform includes --------------------------------*/
#include "port.h"

/* ----------------------- Modbus includes ----------------------------------*/
#include <stdio.h>

#include "mbport.h"



/* ----------------------- Start implementation -----------------------------*/
BOOL
xMBPortTimersInit(USHORT usTim1Timerout50us)
{
	ENTER_CRITICAL_SECTION();

	uint16_t v = usTim1Timerout50us * 50 * 10;

	TCB0.CTRLB = TCB_CNTMODE_INT_gc;
	TCB0.INTCTRL = TCB_CAPT_bm;
	TCB0.CCMP = v;
	TCB0.CTRLA = TCB_CLKSEL_DIV2_gc; // 2MHz / 2 and 1 [CCMP] = 1 [us]

	EXIT_CRITICAL_SECTION();

	return TRUE;
}

void
vMBPortTimersEnable()
{
	TCB0.CNT = 0;
	TCB0.CTRLA |= TCB_ENABLE_bm;
}

void
vMBPortTimersDisable()
{
	TCB0.CTRLA &= ~TCB_ENABLE_bm;
	TCB0.CNT = 0;
}

/* Create an ISR which is called whenever the timer has expired. This function
 * must then call pxMBPortCBTimerExpired( ) to notify the protocol stack that
 * the timer has expired.
 */
void prvvTIMERExpiredISR(void)
{
	(void)pxMBPortCBTimerExpired();
}


ISR(TCB0_INT_vect)
{
	TCB0.INTFLAGS = TCB_CAPT_bm;

	TCB0.CTRLA &= ~TCB_ENABLE_bm;

	prvvTIMERExpiredISR();
}
