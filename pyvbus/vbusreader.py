#!/usr/bin/env python3

import asyncio
import serial
import serial_asyncio
from pyvbus.vbusexception import VBUSException


async def ReadFromSerialAsync(port, source=None, destination=None):
    reader, _ = await serial_asyncio.open_serial_connection(
        url=port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )
    buffer = bytearray()
    await reader.readuntil(b'\xaa')  # wait for message start
    while True:
        buffer = bytearray(b'\xaa')  # initialise new buffer
        buffer.extend(await reader.readuntil(b'\xaa'))
        if len(buffer) >= 5:
            header_destination = buffer[1] + buffer[2] * 0x100
            header_source = buffer[3] + buffer[4] * 0x100
            if source is None or source == header_source:
                if destination is None or destination == header_destination:
                    return buffer[0:len(buffer)-1]
