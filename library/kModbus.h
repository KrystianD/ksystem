#pragma once

#include <stdint.h>

struct ModbusValue
{
	union
	{
		uint16_t u16;
		int16_t s16;
		struct
		{
			uint8_t b0;
			uint8_t b1;
		};
	};

	static ModbusValue U16(uint16_t val) { return { .u16=val }; }
	static ModbusValue S16(int16_t val) { return { .s16=val }; }
};

struct ModbusResult
{
	bool success;
	ModbusValue value;

	static ModbusResult U16(uint16_t val) { return { .success=true, .value=ModbusValue::U16(val) }; }
	static ModbusResult S16(int16_t val) { return { .success=true, .value=ModbusValue::S16(val) }; }
	static ModbusResult Error() { return { .success=false }; }
};

enum class CoilResult
{
	NoCoil,
	High,
	Low,
};

extern ModbusResult modbusHandleReadInputRegister(uint16_t address);

extern ModbusResult modbusHandleReadHoldingRegister(uint16_t address);
extern bool modbusHandleWriteHoldingRegister(uint16_t address, ModbusValue value);

extern CoilResult modbusHandleReadCoil(uint16_t address);
extern bool modbusHandleWriteCoil(uint16_t address, bool enabled);

class kModbus
{
public:
	static void init();
	static void start(uint8_t slaveId);
	static void process();
};

