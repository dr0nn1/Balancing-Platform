#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Communicate with PLC though
Modbus-communication. Sending and
receiving data.

Code by: Magnus Øye, Dated: 05.10-2018
Contact: magnus.oye@gmail.com
Website: https://github.com/magnusoy/Balancing-Platform
"""

# Importing packages
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient


class ModbusClient(object):
    """Establishes a secure connection with the
    Modbus slave. Will be able to read and write
    to all of the available I/O."""
    def __init__(self, ip='192.168.2.17'):
        self.ip = ip
        self.client = ModbusTcpClient(self.ip)
        self.connection = self.client.connect()

    def isConnected(self):
        """Returns the connection status.
        Return: True if connected, False if not."""
        return self.connection

    def sendInt(self, value, address):
        """Send a 32 bit value to the first modbus unit.
        Parameters: value and address where the value will be
        stored in.
        Return: Result if it was successful or not."""
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_32bit_int(value)
        payload = builder.build()
        result = self.client.write_registers(address, payload, skip_encode=True, unit=1)
        return result

    def sendFloat(self, value, address):
        """Send a 32 bit value to the first modbus unit.
        Parameters: value and address where the value will be
        stored in.
        Return: Result if it was successful or not."""
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_32bit_float(value)
        payload = builder.build()
        result = self.client.write_registers(address, payload, skip_encode=True, unit=1)
        return result

    def read(self, address):
        """Reads from a given address from the first modbus unit.
        Parameters: address where the value will be read from.
        Return: The read value in string format."""
        result = self.client.read_holding_registers(address, 2, unit=1)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
        return str(decoder.decode_32bit_float())

    def close(self):
        """Closes the connection with the port.
        Return: True when the connection is closed."""
        self.client.close()
        return True


# Simple example of usage
if __name__ == '__main__':
    client = ModbusClient()
    while client.isConnected():
        client.read(address=12288)
