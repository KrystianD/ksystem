#include <kModbus.h>

#include <mb.h>
#include <mbport.h>

int16_t swapS16(int16_t val)
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
	for (uint16_t i = 0; i < usNRegs; i++) {
		ModbusResult val = modbusHandleReadInputRegister(usAddress + i);
		if (!val.success)
			return MB_ENOREG;
		pucRegBuffer[i * 2 + 0] = val.value.b1;
		pucRegBuffer[i * 2 + 1] = val.value.b0;
	}

	return MB_ENOERR;
}

eMBErrorCode eMBRegHoldingCB(UCHAR* pucRegBuffer, USHORT usAddress, USHORT usNRegs, eMBRegisterMode eMode)
{
	if (eMode == MB_REG_READ) {
		for (uint16_t i = 0; i < usNRegs; i++) {
			ModbusResult val = modbusHandleReadHoldingRegister(usAddress + i);
			if (!val.success)
				return MB_ENOREG;
			pucRegBuffer[i * 2 + 0] = val.value.b1;
			pucRegBuffer[i * 2 + 1] = val.value.b0;
		}
	}
	else {
		for (uint16_t i = 0; i < usNRegs; i++) {
			uint16_t value = swapS16(((uint16_t*)pucRegBuffer)[i]);
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
				case CoilResult::NoCoil: return MB_ENOREG;
				case CoilResult::High: pucRegBuffer[i / 8] |= 1 << (i % 8);
					break;
				case CoilResult::Low: pucRegBuffer[i / 8] &= ~(1 << (i % 8));
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
