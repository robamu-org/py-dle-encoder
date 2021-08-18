from unittest import TestCase
import dle_encoder


START_MARKER = dle_encoder.STX_CHAR
END_MARKER = dle_encoder.ETX_CHAR
DLE_CHAR = dle_encoder.DLE_CHAR
TEST_ARRAY_0 = bytearray(5)
TEST_ARRAY_1 = bytearray([0x00, DLE_CHAR, 0x00])
TEST_ARRAY_2 = bytearray([0x00, START_MARKER, 0x00])
TEST_ARRAY_3 = bytearray([0x00, dle_encoder.CARRIAGE_RETURN, START_MARKER])


class TestEncoder(TestCase):
    def test_encoding(self):
        encoder = dle_encoder.DleEncoder()
        encoded = encoder.encode(TEST_ARRAY_0)
        expected = bytearray()
        expected.append(START_MARKER)
        expected.extend(TEST_ARRAY_0)
        expected.append(END_MARKER)
        self.assertEqual(encoded, expected)

        encoded = encoder.encode(TEST_ARRAY_1)
        expected = bytearray()
        expected.append(START_MARKER)
        expected.append(0x00)
        expected.append(DLE_CHAR)
        expected.append(DLE_CHAR)
        expected.append(0x00)
        expected.append(END_MARKER)
        self.assertEqual(encoded, expected)

        encoded = encoder.encode(TEST_ARRAY_2)
        expected = bytearray()
        expected.append(START_MARKER)
        expected.append(0x00)
        expected.append(DLE_CHAR)
        expected.append(START_MARKER + 0x40)
        expected.append(0x00)
        expected.append(END_MARKER)
        self.assertEqual(encoded, expected)

        encoder.escape_cr = True
        encoded = encoder.encode(TEST_ARRAY_3, add_stx_etx=True)
        expected = bytearray()
        expected.append(START_MARKER)
        expected.append(0x00)
        expected.append(DLE_CHAR)
        expected.append(dle_encoder.CARRIAGE_RETURN + 0x40)
        expected.append(DLE_CHAR)
        expected.append(START_MARKER + 0x40)
        expected.append(END_MARKER)
        self.assertEqual(encoded, expected)

    def test_decoding(self):
        encoder = dle_encoder.DleEncoder()
        self.generic_decoding_test(encoder=encoder, array=TEST_ARRAY_0)
        self.generic_decoding_test(encoder=encoder, array=TEST_ARRAY_1)
        self.generic_decoding_test(encoder=encoder, array=TEST_ARRAY_2)
        encoder.escape_cr = True
        self.generic_decoding_test(encoder=encoder, array=TEST_ARRAY_3)

        # End marker invalid. Everything except end marker is decoded
        encoded = encoder.encode(TEST_ARRAY_2)
        encoded[len(encoded) - 1] = 0x00
        err_code, decoded, bytes_decoded = encoder.decode(encoded)
        self.assertEqual(err_code, dle_encoder.DleErrorCodes.DECODING_ERROR)
        self.assertEqual(bytes_decoded, len(encoded) - 1)

        # Start byte invalid. Nothing is decoded
        encoded = encoder.encode(TEST_ARRAY_1)
        encoded[0] = 0x00
        err_code, decoded, bytes_decoded = encoder.decode(encoded)
        self.assertEqual(err_code, dle_encoder.DleErrorCodes.DECODING_ERROR)
        self.assertEqual(bytes_decoded, 0)

        # Second value after DLE not properly escaped, so only two bytes are decoded
        encoded = encoder.encode(TEST_ARRAY_2)
        encoded[3] = 0x00
        err_code, decoded, bytes_decoded = encoder.decode(encoded)
        self.assertEqual(err_code, dle_encoder.DleErrorCodes.DECODING_ERROR)
        self.assertEqual(bytes_decoded, 2)

    def generic_decoding_test(
            self, encoder: dle_encoder.DleEncoder, array: bytearray
    ):
        encoded = encoder.encode(array)
        err_code, decoded, bytes_decoded = encoder.decode(encoded)
        self.assertEqual(err_code, dle_encoder.DleErrorCodes.OK)
        self.assertEqual(array, decoded)
        self.assertEqual(bytes_decoded, len(encoded))
