#pragma once

#include <avr/io.h>

#include <stdint.h>

extern void kSysTickElapsed();

template<int Period>
class kSysTick
{
	volatile uint16_t _ticks = 0;

public:
	constexpr void init()
	{
		loop_until_bit_is_clear(RTC.STATUS, RTC_PERBUSY_bp);
		RTC.PER = Period - 1;
		RTC.INTCTRL = RTC_OVF_bm;
		RTC.CLKSEL = RTC_CLKSEL_INT32K_gc;
		loop_until_bit_is_clear(RTC.STATUS, RTC_CTRLABUSY_bp);
		RTC.CTRLA = RTC_RTCEN_bm | RTC_PRESCALER_DIV1_gc;
	}

	constexpr void handleInterrupt()
	{
		_ticks++;
		RTC.INTFLAGS = RTC_OVF_bm;
	}

	constexpr uint16_t ticks()
	{
		return _ticks;
	}
};
