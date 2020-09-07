#pragma once

#include <avr/io.h>

#include <stdint.h>

#define PIN_FROM_PORT(port) _SFR_IO8(_SFR_IO_ADDR(port) - 2)
#define DDR_FROM_PORT(port) _SFR_IO8(_SFR_IO_ADDR(port) - 1)
#define PORT_FROM_PORT(port) _SFR_IO8(_SFR_IO_ADDR(port))

template<uint16_t PortAddr, uint8_t Pin>
class kGPIO
{
public:
	void input() { DDR_FROM_PORT(_SFR_IO8(PortAddr)) &= ~(1u << Pin); }
	void pushPull() { DDR_FROM_PORT(_SFR_IO8(PortAddr)) |= 1u << Pin; }
	void high() { _SFR_IO8(PortAddr) |= 1u << Pin; }
	void low() { _SFR_IO8(PortAddr) &= ~(1u << Pin); }
	void toggle() { _SFR_IO8(PortAddr) ^= 1u << Pin; }

	void inputPullup()
	{
		input();
		high();
	}

	bool read() { return PIN_FROM_PORT(_SFR_IO8(PortAddr)) & (1u << Pin); }
};

