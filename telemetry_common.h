// Copyright (C) 2026 Hector van der Aa <hector@h3cx.dev>
// Copyright (C) 2026 Association Exergie <association.exergie@gmail.com>
// SPDX-License-Identifier: MIT
#pragma once
#include <inttypes.h>

#pragma pack(push, 1)
struct TelemetryPacket1 {
  char ping_[4] = {'P', 'I', 'N', 'G'};
};
#pragma pack(pop)

#pragma pack(push, 1)
struct TelemetryPacket2 {
  float vbat;
  float teng;
  float lat;
  float lng;
  float speed;
};
#pragma pack(pop)

#pragma pack(push, 1)
struct TelemetryLoRaHeader {
  uint8_t source_;
  uint8_t dest_;
  uint8_t version_;
  uint8_t size_;
  uint16_t crc16_;
};
#pragma pack(pop)

#pragma pack(push, 1)
struct TelemetryUARTHeader {
  uint8_t magic_[4] = {0xAA, 0x55, 0xAA, 0x55};
  uint8_t size_;
};
#pragma pack(pop)

uint16_t crc16_ccitt(const uint8_t *data, uint16_t length);
