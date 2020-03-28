#include <port.h>
#include <util/crc16.h>

USHORT
usMBCRC16(UCHAR* pucFrame, USHORT usLen)
{
	uint16_t crc = 0xffff;

	for (uint16_t i = 0; i < usLen; i++)
		crc = _crc16_update(crc, pucFrame[i]);

	return crc;
}
