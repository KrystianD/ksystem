#pragma once

#include <stdint.h>

uint16_t swapU16(uint16_t val);

struct ModbusReturnValue
{
	uint16_t* buffer;
	uint16_t* pIdx;

	bool U16(uint16_t val)
	{
		buffer[0] = swapU16(val);
		*pIdx += 1;
		return true;
	}
	bool S16(int16_t val)
	{
		buffer[0] = swapU16(val);
		*pIdx += 1;
		return true;
	}
	bool U32LE(uint32_t val)
	{
		uint16_t* pVal = (uint16_t*)&val;
		buffer[0] = swapU16(pVal[0]);
		buffer[1] = swapU16(pVal[1]);
		*pIdx += 2;
		return true;
	}
	bool U32BE(uint32_t val)
	{
		uint16_t* pVal = (uint16_t*)&val;
		buffer[0] = swapU16(pVal[1]);
		buffer[1] = swapU16(pVal[0]);
		*pIdx += 2;
		return true;
	}
	bool S32LE(int32_t val)
	{
		uint16_t* pVal = (uint16_t*)&val;
		buffer[0] = swapU16(pVal[0]);
		buffer[1] = swapU16(pVal[1]);
		*pIdx += 2;
		return true;
	}
	bool S32BE(int32_t val)
	{
		uint16_t* pVal = (uint16_t*)&val;
		buffer[0] = swapU16(pVal[1]);
		buffer[1] = swapU16(pVal[0]);
		*pIdx += 2;
		return true;
	}
	bool FLOATBE(float val)
	{
		uint16_t* pVal = (uint16_t*)&val;
		buffer[0] = swapU16(pVal[1]);
		buffer[1] = swapU16(pVal[0]);
		*pIdx += 2;
		return true;
	}
};

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

	static ModbusValue U16(uint16_t val)
	{
		ModbusValue value;
		value.u16 = val;
		return value;
	}
	static ModbusValue S16(int16_t val)
	{
		ModbusValue value;
		value.s16 = val;
		return value;
	}
};

struct ModbusResult
{
	bool success;
	ModbusValue value;

	static ModbusResult U16(uint16_t val) { return { .success = true, .value = ModbusValue::U16(val) }; }
	static ModbusResult S16(int16_t val) { return { .success = true, .value = ModbusValue::S16(val) }; }
	static ModbusResult Error() { return { .success = false }; }
};

enum class CoilResult
{
	NoCoil,
	High,
	Low,
};

extern bool modbusHandleReadInputRegister(uint16_t address, ModbusReturnValue& value);

extern bool modbusHandleReadHoldingRegister(uint16_t address, ModbusReturnValue& value);
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
