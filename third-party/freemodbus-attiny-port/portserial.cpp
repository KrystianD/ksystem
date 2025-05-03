#include "port.h"

/* ----------------------- Modbus includes ----------------------------------*/
#include <ksystem.h>
#include <ksystem_internal.h>

#include "mbport.h"

void
vMBPortSerialEnable(BOOL xRxEnable, BOOL xTxEnable)
{
	ENTER_CRITICAL_SECTION();

	if (xTxEnable) {
		MODBUS_SERIAL.Device()->CTRLA |= USART_DREIE_bm;
	}
	else {
		MODBUS_SERIAL.Device()->CTRLA &= ~USART_DREIE_bm;
	}

	EXIT_CRITICAL_SECTION();
}

BOOL
xMBPortSerialInit(UCHAR ucPORT, ULONG ulBaudRate, UCHAR ucDataBits, eMBParity eParity)
{
	MODBUS_SERIAL.Device()->CTRLA |= USART_RXCIE_bm;
	return TRUE;
}

BOOL
xMBPortSerialPutByte(CHAR ucByte)
{
	MODBUS_SERIAL.Device()->TXDATAL = ucByte;
	return TRUE;
}

BOOL
xMBPortSerialGetByte(CHAR* pucByte)
{
	*pucByte = MODBUS_SERIAL.Device()->RXDATAL;
	return TRUE;
}
