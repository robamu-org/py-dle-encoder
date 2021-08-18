[![Documentation Status](https://readthedocs.org/projects/dle-encoder/badge/?version=latest)](https://dle-encoder.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/robamu-org/py-dle-encoder/branch/main/graph/badge.svg?token=GQ5VW8PKKS)](https://codecov.io/gh/robamu-org/py-dle-encoder)

DLE Encoder for Python
======

This encoder provides a simple ASCII transport layer for serial data.
A give data stream is encoded by adding a STX (0x02) char at the beginning and an ETX (0x03) char at the end.
All STX and ETX occurrences in the packet are encoded as well so the receiver can simply look for STX and ETX
occurrences to identify packets.

There are two modes for the encoder:

## Escaped mode

The encoded stream starts with a STX marker and ends with an ETX marker.
STX and ETX occurrences in the stream are escaped and internally encoded as well so the
receiver side can simply check for STX and ETX markers as frame delimiters. When using a
strictly char based reception of packets encoded with DLE,
STX can be used to notify a reader that actual data will start to arrive
while ETX can be used to notify the reader that the data has ended.

## Non-escaped mode

The encoded stream starts with DLE STX and ends with DLE ETX. All DLE occurrences in the stream
are escaped with DLE. If the receiver detects a DLE char, it needs to read the next char
to determine whether a start (STX) or end (ETX) of a frame has been detected.

You can find a C++ implementation
[here](https://egit.irs.uni-stuttgart.de/fsfw/fsfw/src/branch/master/globalfunctions/DleEncoder.cpp).

# Install

You can install this package from PyPI

Linux:

```sh
python3 -m pip install dle-encoder
```

Windows:

```sh
py -m pip install dle-encoder
```

# Examples

```py
import dle_encoder

encoder = dle_encoder.DleEncoder()
test_array = bytearray([1, 2, 3])
encoded = encoder.encode(test_array)
retval, decoded, bytes_decoded = encoder.decode(encoded)

print(test_array)
print(encoded)
print(decoded)
```

The non-escaped mode can be used by passing `escape_stx_etc=False` to the
`DleEncoder` constructor.
