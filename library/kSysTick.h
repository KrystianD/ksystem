#pragma once

#include <avr/io.h>
#include <util/atomic.h>

#include <stdint.h>

template<int Overflows, int Remainder>
class kSysTick
{
	volatile static uint8_t _overflowCounter;
	volatile static uint16_t _ticks;
	volatile static uint8_t _nextStep;

public:
	static void init() {
		if (Overflows == 0)
			OCR2 = Remainder - 1;
		else
			OCR2 = 255;
	}

	static void handleInterrupt()
	{
		if (Overflows == 0) {
			OCR2 = Remainder - 1;
			_nextStep = 1;
			_ticks++;
		}
		else {
			if (_overflowCounter == Overflows) {
				OCR2 = 255;
				_overflowCounter = 0;
				_nextStep = 1;
				_ticks++;
			}
			else if (_overflowCounter == Overflows - 1) {
				OCR2 = Remainder - 1;
				_overflowCounter++;
			}
			else {
				_overflowCounter++;
			}
		}
	}


	static bool elapsed()
	{
		uint8_t didElapsed;
		ATOMIC_BLOCK(ATOMIC_FORCEON) {
			didElapsed = _nextStep == 1;
			_nextStep = 0;
		}
		return didElapsed;
	}

	static uint16_t ticks()
	{
		return _ticks;
	}
};

