#pragma once

#include <kCommon.h>

#include <avr/io.h>
#include <avr/common.h>

#include <stdint.h>

class kSerial
{
public:
	static void put(char c)
	{
		while (bit_is_clear(UCSRA, UDRE));
		UDR = c;
	}

	static char get()
	{
		while (bit_is_clear(UCSRA, RXC));
		return UDR;
	}

	static void enableTx() { sbi(UCSRB, TXEN); }
	static void disableTx() { cbi(UCSRB, TXEN); }

	static void enableRx() { sbi(UCSRB, RXEN); }
	static void disableRx() { cbi(UCSRB, RXEN); }

	static void enableTxCompletionInterrupt() { sbi(UCSRB, TXCIE); }
	static void disableTxCompletionInterrupt() { cbi(UCSRB, TXCIE); }

	static void enableRxCompletionInterrupt() { sbi(UCSRB, RXCIE); }
	static void disableRxCompletionInterrupt() { cbi(UCSRB, RXCIE); }

	static void enableRxDataReadyInterrupt() { sbi(UCSRB, UDRE); }
	static void disableRxDataReadyInterrupt() { cbi(UCSRB, UDRE); }
};

