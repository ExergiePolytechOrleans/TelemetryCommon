# Copyright (C) 2026 Hector van der Aa <hector@h3cx.dev>
# Copyright (C) 2026 Association Exergie <association.exergie@gmail.com>
# SPDX-License-Identifier: MIT
import struct
from dataclasses import dataclass

UART_MAGIC = b"\xAA\x55\xAA\x55"

LORA_HEADER_FORMAT = "<BBBBH"
UART_HEADER_FORMAT = "<4sB"
PACKET1_FORMAT = "<4s"
PACKET2_FORMAT = "<Ifffff"

LORA_HEADER_SIZE = struct.calcsize(LORA_HEADER_FORMAT)
UART_HEADER_SIZE = struct.calcsize(UART_HEADER_FORMAT)
PACKET1_SIZE = struct.calcsize(PACKET1_FORMAT)
PACKET2_SIZE = struct.calcsize(PACKET2_FORMAT)


@dataclass
class TelemetryLoRaHeader:
    source: int
    dest: int
    version: int
    size: int
    crc16: int


@dataclass
class TelemetryPacket1:
    ping: bytes


@dataclass
class TelemetryPacket2:
    time_stamp: int
    vbat: float
    teng: float
    lat: float
    lng: float
    speed: float


def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def unpack_lora_header(data: bytes) -> TelemetryLoRaHeader:
    source, dest, version, size, crc16 = struct.unpack(LORA_HEADER_FORMAT, data[:LORA_HEADER_SIZE])
    return TelemetryLoRaHeader(source, dest, version, size, crc16)


def unpack_packet1(payload: bytes) -> TelemetryPacket1:
    (ping,) = struct.unpack(PACKET1_FORMAT, payload[:PACKET1_SIZE])
    return TelemetryPacket1(ping)


def unpack_packet2(payload: bytes) -> TelemetryPacket2:
    time_stamp, vbat, teng, lat, lng, speed = struct.unpack(PACKET2_FORMAT, payload[:PACKET2_SIZE])
    return TelemetryPacket2(time_stamp, vbat, teng, lat, lng, speed)
