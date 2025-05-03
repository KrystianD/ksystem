#pragma once

#include <avr/io.h>
#include <util/atomic.h>

#include <stdint.h>

template<int SysTickInterval, void(* ElapsedCallback)(), bool AutoRestart>
class kSysTimer
{
	volatile uint16_t _initial;
	volatile uint16_t _remaining;
	volatile uint8_t _elapsed;

public:
	void start(uint16_t timeout)
	{
		ATOMIC_BLOCK(ATOMIC_FORCEON)
		{
			if (AutoRestart)
				_initial = timeout;
			_remaining = timeout;
		}
	}

	void stop()
	{
		ATOMIC_BLOCK(ATOMIC_FORCEON)
		{
			_remaining = 0;
			_elapsed = 0;
		}
	}

	uint16_t remaining() { return _remaining; }

	bool elapsed()
	{
		uint8_t didElapsed;
		ATOMIC_BLOCK(ATOMIC_FORCEON)
		{
			didElapsed = _elapsed == 1;
			_elapsed = 0;
		}
		return didElapsed;
	}

private:
	void handleTick()
	{
		if (_remaining == 0)
			return;

		if (_remaining < SysTickInterval)
			_remaining = 0;
		else
			_remaining -= SysTickInterval;

		if (_remaining == 0) {
			_elapsed = 1;
			if (AutoRestart) {
				_remaining = _initial;
			}
		}
	}

	void process()
	{
		if (ElapsedCallback)
			if (elapsed())
				ElapsedCallback();
	}

	friend int main();
	friend void kSysTickElapsed();
};

