#!/usr/bin/env python3


import unittest

import vbuspacket


class TestException(unittest.TestCase):

    def test_parsingexception(self):
        # missing sync byte
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(
                bytearray.fromhex("000000000000000000")
            )
        )
        # buffer to small (less than 6)
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(bytearray.fromhex("aa00000000"))
        )
        # invalid protocol
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(bytearray.fromhex("aa0000000030"))
        )

    def test_parsingprotocol1(self):
        # buffer to small (less than 10)
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(bytearray.fromhex("aa0000000010"))
        )
        # invalid header checksum
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(
                bytearray.fromhex("aa000000001000000000")
            )
        )
        # invalid frame count
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(
                bytearray.fromhex("aa00000000100000016e")
            )
        )
        # MSB not allowed
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(
                bytearray.fromhex("aa00000000100000016eff0000000000")
            )
        )
        # invalid frame checksum
        self.assertRaises(
            vbuspacket.VBUSPacketException,
            lambda: vbuspacket.VBUSPacket(
                bytearray.fromhex("aa00000000100000016e000000000000")
            )
        )
        # valid fake packet
        self.assertIsInstance(
            vbuspacket.VBUSPacket(
                bytearray.fromhex("aa00000000100000016e00000000007f")
            ),
            vbuspacket.VBUSPacket
        )


class Test_0x7321(unittest.TestCase):

    def setUp(self):
        hexbuffer = 'aa100021731000011238'
        hexbuffer += '5d000000041e0c001501015c5b012801007a25013822047b'
        hexbuffer += '7c03382204223822382205465d020000011f00000000007f'
        hexbuffer += '00000000007f000e000001703b000000004400000000007f'
        hexbuffer += '00000000007f00000000007f00002d00005200000000007f'
        hexbuffer += '01034503042f02000000007d'
        self.packet = vbuspacket.VBUSPacket(bytearray.fromhex(hexbuffer))

    def test_header(self):
        self.assertEqual(0x0010, self.packet.header_destination)
        self.assertEqual(0x7321, self.packet.header_source)
        self.assertEqual(0x10, self.packet.header_protocol)
        self.assertEqual(0x0100, self.packet.header_command)
        self.assertEqual(0x12, self.packet.header_framecount)
        self.assertEqual(0x38, self.packet.header_checksum)

    def test_rawvalues(self):
        # Temperatur Sensor 1-12
        self.assertEqual(93, self.packet.GetRawValue(0, 2))
        self.assertEqual(128, self.packet.GetRawValue(2, 2))
        self.assertEqual(140, self.packet.GetRawValue(4, 2))
        self.assertEqual(277, self.packet.GetRawValue(6, 2))
        self.assertEqual(347, self.packet.GetRawValue(8, 2))
        self.assertEqual(296, self.packet.GetRawValue(10, 2))
        self.assertEqual(293, self.packet.GetRawValue(12, 2))
        self.assertEqual(8888, self.packet.GetRawValue(14, 2))
        self.assertEqual(892, self.packet.GetRawValue(16, 2))
        self.assertEqual(8888, self.packet.GetRawValue(18, 2))
        self.assertEqual(8888, self.packet.GetRawValue(20, 2))
        self.assertEqual(8888, self.packet.GetRawValue(22, 2))
        # Einstrahlung
        self.assertEqual(733, self.packet.GetRawValue(24, 2))
        # Impulseingang 1-2
        self.assertEqual(0, self.packet.GetRawValue(28, 4))
        self.assertEqual(0, self.packet.GetRawValue(32, 4))
        # Sensor Maske
        self.assertEqual(3712, self.packet.GetRawValue(36, 2))
        self.assertEqual(0, self.packet.GetRawValue(38, 2))
        self.assertEqual(59, self.packet.GetRawValue(40, 2))
        # Drehzahl Relais 1-9
        self.assertEqual(0, self.packet.GetRawValue(44, 1))
        self.assertEqual(0, self.packet.GetRawValue(45, 1))
        self.assertEqual(0, self.packet.GetRawValue(46, 1))
        self.assertEqual(0, self.packet.GetRawValue(47, 1))
        self.assertEqual(0, self.packet.GetRawValue(48, 1))
        self.assertEqual(0, self.packet.GetRawValue(49, 1))
        self.assertEqual(0, self.packet.GetRawValue(50, 1))
        self.assertEqual(0, self.packet.GetRawValue(51, 1))
        self.assertEqual(0, self.packet.GetRawValue(52, 1))
        # System
        self.assertEqual(45, self.packet.GetRawValue(58, 2))
        self.assertEqual(0, self.packet.GetRawValue(60, 2))
        self.assertEqual(0, self.packet.GetRawValue(62, 2))
        self.assertEqual(769, self.packet.GetRawValue(64, 2))
        self.assertEqual(965, self.packet.GetRawValue(66, 2))

    def test_temperaturevalues(self):
        # Temperatur Sensor 1-12
        self.assertEqual(9.3, self.packet.GetTemperatureValue(0, 2))
        self.assertEqual(12.8, self.packet.GetTemperatureValue(2, 2))
        self.assertEqual(14.0, self.packet.GetTemperatureValue(4, 2))
        self.assertEqual(27.7, self.packet.GetTemperatureValue(6, 2))
        self.assertEqual(34.7, self.packet.GetTemperatureValue(8, 2))
        self.assertEqual(29.6, self.packet.GetTemperatureValue(10, 2))
        self.assertEqual(29.3, self.packet.GetTemperatureValue(12, 2))
        self.assertEqual(888.8, self.packet.GetTemperatureValue(14, 2))
        self.assertEqual(89.2, self.packet.GetTemperatureValue(16, 2))
        self.assertEqual(888.8, self.packet.GetTemperatureValue(18, 2))
        self.assertEqual(888.8, self.packet.GetTemperatureValue(20, 2))
        self.assertEqual(888.8, self.packet.GetTemperatureValue(22, 2))

    def test_timevalues(self):
        self.assertEqual('16:05', self.packet.GetTimeValue(66, 2))


if __name__ == '__main__':
    unittest.main()
