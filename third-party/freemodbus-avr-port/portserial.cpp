/*
 * FreeModbus Libary: ATMega168 Port
 * Copyright (C) 2006 Christian Walter <wolti@sil.at>
 *   - Initial version and ATmega168 support
 * Modfications Copyright (C) 2006 Tran Minh Hoang:
 *   - ATmega8, ATmega16, ATmega32 support
 *   - RS485 support for DS75176
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * File: $Id$
 */

#include <avr/io.h>
#include <avr/interrupt.h>

#include "port.h"

/* ----------------------- Modbus includes ----------------------------------*/
#include "mb.h"
#include "mbport.h"

#include <ksystem.h>

#define UART_BAUD_RATE          9600
#define UART_BAUD_CALC(UART_BAUD_RATE,F_OSC) \
    ( ( F_OSC ) / ( ( UART_BAUD_RATE ) * 16UL ) - 1 )

//#define UART_UCSRB  UCSR0B

void
vMBPortSerialEnable( BOOL xRxEnable, BOOL xTxEnable )
{
#ifdef MODBUS_RS485_DIR_PIN
    Serial.enableTxCompletionInterrupt();
#endif

    if( xRxEnable )
    {
        Serial.enableRxCompletionInterrupt();
        Serial.enableRx();
    }
    else
    {
        Serial.disableRxCompletionInterrupt();
        Serial.disableRx();
    }

    if( xTxEnable )
    {
        Serial.enableRxDataReadyInterrupt();
#ifdef MODBUS_RS485_DIR_PIN
        RTS_HIGH;
#endif
    }
    else
    {
        Serial.disableRxDataReadyInterrupt();
    }
}

BOOL
xMBPortSerialInit( UCHAR ucPORT, ULONG ulBaudRate, UCHAR ucDataBits, eMBParity eParity )
{
	  Serial.enableTx();
    vMBPortSerialEnable( FALSE, FALSE );
#ifdef MODBUS_RS485_DIR_PIN
    RTS_INIT;
#endif
    return TRUE;
}

BOOL
xMBPortSerialPutByte( CHAR ucByte )
{
    Serial.put(ucByte);
    return TRUE;
}

BOOL
xMBPortSerialGetByte( CHAR * pucByte )
{
    *pucByte = Serial.get();
    return TRUE;
}

SIGNAL( USART_UDRE_vect )
{
    pxMBFrameCBTransmitterEmpty(  );
}

SIGNAL( USART_RXC_vect )
{
    pxMBFrameCBByteReceived(  );
}

#ifdef MODBUS_RS485_DIR_PIN
SIGNAL( USART_TXC_vect )
{
    RTS_LOW;
}
#endif

