#pragma once

#include <avr/io.h>

#include <stdint.h>

class kSerial
{
public:
	static void put(char c)
	{
		while (bit_is_clear (UCSRA, UDRE));
		UDR = c;
	}
};

