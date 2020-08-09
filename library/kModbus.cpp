#include <kModbus.h>

#include <mb.h>
#include <mbport.h>

uint16_t swapU16(uint16_t val)
{
	return (val << 8) | ((val >> 8) & 0xFF);
}

void kModbus::init()
{
}

void kModbus::start(uint8_t slaveId)
{
	eMBErrorCode eStatus;

	eStatus = eMBInit(MB_RTU, slaveId, 0, 9600, MB_PAR_NONE);
	eStatus = eMBEnable();
}

void kModbus::process()
{
	eMBPoll();
}

eMBErrorCode eMBRegInputCB(UCHAR* pucRegBuffer, USHORT usAddress, USHORT usNRegs)
{
	uint16_t* wordPtr = (uint16_t*)pucRegBuffer;

	for (uint16_t i = 0; i < usNRegs;) {
		ModbusReturnValue value = { .buffer = &wordPtr[i], .pIdx=&i };
		bool res = modbusHandleReadInputRegister(usAddress + i, value);
		if (!res)
			return MB_ENOREG;
#endif
	}

	return MB_ENOERR;
}

eMBErrorCode eMBRegHoldingCB(UCHAR* pucRegBuffer, USHORT usAddress, USHORT usNRegs, eMBRegisterMode eMode)
{
	uint16_t* wordPtr = (uint16_t*)pucRegBuffer;

	if (eMode == MB_REG_READ) {
		for (uint16_t i = 0; i < usNRegs;) {
			ModbusReturnValue value = { .buffer = &wordPtr[i], .pIdx=&i };
			bool res = modbusHandleReadHoldingRegister(usAddress + i, value);
			if (!res)
				return MB_ENOREG;
#endif
		}
	}
	else {
		for (uint16_t i = 0; i < usNRegs; i++) {
			uint16_t value = swapU16(wordPtr[i]);
			if (!modbusHandleWriteHoldingRegister(usAddress + i, ModbusValue::U16(value)))
				return MB_ENOREG;
		}
	}

	return MB_ENOERR;
}

eMBErrorCode eMBRegCoilsCB(UCHAR* pucRegBuffer, USHORT usAddress, USHORT usNCoils, eMBRegisterMode eMode)
{
	if (eMode == MB_REG_READ) {
		for (uint16_t i = 0; i <= i / 8; i++)
			pucRegBuffer[i] = 0;

		for (uint16_t i = 0; i < usNCoils; i++) {
			CoilResult res = modbusHandleReadCoil(usAddress + i);

			switch (res) {
				case CoilResult::NoCoil:
					return MB_ENOREG;
				case CoilResult::High:
					pucRegBuffer[i / 8] |= 1 << (i % 8);
					break;
				case CoilResult::Low:
					pucRegBuffer[i / 8] &= ~(1 << (i % 8));
					break;
			}
		}
	}
	else {
		for (uint16_t i = 0; i < usNCoils; i++)
			if (!modbusHandleWriteCoil(usAddress + i, pucRegBuffer[i / 8] & (1 << (i % 8))))
				return MB_ENOREG;
	}

	return MB_ENOERR;
}

//eMBErrorCode eMBRegDiscreteCB(UCHAR* pucRegBuffer, USHORT usAddress, USHORT usNDiscrete)
//{
//	return MB_ENOREG;
//}
