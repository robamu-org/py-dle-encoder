"""DLE Encoder Implementation
This encoder provides a simple ASCII transport layer for serial data.
A give data stream is encoded by adding a STX char at the beginning and an ETX char at the end.
All STX and ETX occurrences in the packet are encoded as well so the receiver can simply look
for STX and ETX occurrences to identify packets.
You can find a C++ implementation here:
https://egit.irs.uni-stuttgart.de/fsfw/fsfw/src/branch/master/globalfunctions/DleEncoder.cpp
"""
import enum
from typing import Tuple

STX_CHAR = 0x02
ETX_CHAR = 0x03
CARRIAGE_RETURN = 0x0D
DLE_CHAR = 0x10


class DleErrorCodes(enum.Enum):
    OK = 0,
    DECODING_ERROR = 1


def encode_dle(
        source_packet: bytearray, add_stx_etx: bool = True, encode_cr: bool = False
) -> bytearray:
    """Encodes a given stream with DLE encoding.
    :return: Returns a tuple with 2 values.
    - DleErrorCode, which should be DleErrorCodes.OK for successful encoding
    - Encoded bytearray
    """
    dest_stream = bytearray()
    source_len = len(source_packet)
    source_index = 0
    if add_stx_etx:
        dest_stream.append(STX_CHAR)

    while source_index < source_len:
        next_byte = source_packet[source_index]
        # STX, ETX and CR characters in the stream need to be escaped with DLE
        if (next_byte == STX_CHAR or next_byte == ETX_CHAR) or \
                (encode_cr and next_byte == CARRIAGE_RETURN):
            dest_stream.append(DLE_CHAR)
            """Escaped byte will be actual byte + 0x40. This prevents
            STX and ETX characters from appearing
            in the encoded data stream at all, so when polling an
            encoded stream, the transmission can be stopped at ETX.
            0x40 was chosen at random with special requirements:
            - Prevent going from one control char to another
            - Prevent overflow for common characters
            """
            dest_stream.append(next_byte + 0x40)
        elif next_byte == DLE_CHAR:
            dest_stream.append(DLE_CHAR)
            dest_stream.append(DLE_CHAR)
        else:
            dest_stream.append(next_byte)
        source_index += 1
    if add_stx_etx:
        dest_stream.append(ETX_CHAR)
    return dest_stream


def decode_dle(
        source_packet: bytearray, decode_cr: bool = False
) -> Tuple[DleErrorCodes, bytearray, int]:
    """Decodes a given DLE encoded data stream. This call only returns the first packet found.

    It might be necessary to call this function multiple times, depending on the third
    return value
    :return:
    Returns a tuple of three values.
    - DleErrorCode: If decoding has failed, this will not be DleErrorCodes.OK. The function
      will still return the read length and the decoded bytearray, if any decoding was performed
    - Decoded bytearray: Decoded packet
    - Read length: Read length in the encoded stream. If this is smaller than the length of
      the passed bytearray, the decoding function should be called again.
    """
    encoded_index = 0
    source_len = len(source_packet)
    dest_stream = bytearray()
    if source_packet[encoded_index] != STX_CHAR:
        return DleErrorCodes.DECODING_ERROR, dest_stream, 0
    encoded_index += 1

    while encoded_index < source_len - 1 and source_packet[encoded_index] != ETX_CHAR \
            and source_packet[encoded_index] != STX_CHAR:
        if source_packet[encoded_index] == DLE_CHAR:
            next_byte = source_packet[encoded_index + 1]
            if next_byte == DLE_CHAR:
                dest_stream.append(next_byte)
            else:
                if (next_byte == 0x42 or next_byte == 0x43) or (decode_cr and next_byte == 0x4D):
                    dest_stream.append(next_byte - 0x40)
                else:
                    return DleErrorCodes.DECODING_ERROR, dest_stream, encoded_index
            encoded_index += 1
        else:
            dest_stream.append(source_packet[encoded_index])
        encoded_index += 1

    if source_packet[encoded_index] != ETX_CHAR:
        return DleErrorCodes.DECODING_ERROR, dest_stream, encoded_index
    else:
        encoded_index += 1
        return DleErrorCodes.OK, dest_stream, encoded_index
