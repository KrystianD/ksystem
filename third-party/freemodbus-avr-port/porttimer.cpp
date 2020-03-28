/*
 * FreeModbus Libary: ATMega168 Port
 * Copyright (C) 2006 Christian Walter <wolti@sil.at>
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

/* ----------------------- AVR includes -------------------------------------*/
#include <avr/io.h>
#include <avr/interrupt.h>

/* ----------------------- Platform includes --------------------------------*/
#include "port.h"

/* ----------------------- Modbus includes ----------------------------------*/
#include "mb.h"
#include "mbport.h"

#include <ksystem.h>

/* ----------------------- Static variables ---------------------------------*/
static USHORT   usTimerMS;

/* ----------------------- Start implementation -----------------------------*/
BOOL
xMBPortTimersInit( USHORT usTim1Timerout50us )
{
    usTimerMS = usTim1Timerout50us / 20;

    vMBPortTimersDisable(  );

    return TRUE;
}

void
vMBPortTimersEnable(  )
{
    modbusTimer.start(usTimerMS);
}

void
vMBPortTimersDisable(  )
{
    modbusTimer.stop();
}

void modbusTimerElapsed()
{
    ( void )pxMBPortCBTimerExpired(  );
}
