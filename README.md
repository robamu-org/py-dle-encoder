[![package](https://github.com/robamu-org/py-dle-encoder/actions/workflows/package.yml/badge.svg)](https://github.com/robamu-org/py-dle-encoder/actions/workflows/package.yml)
[![Documentation Status](https://readthedocs.org/projects/dle-encoder/badge/?version=latest)](https://dle-encoder.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/robamu-org/py-dle-encoder/branch/main/graph/badge.svg?token=GQ5VW8PKKS)](https://codecov.io/gh/robamu-org/py-dle-encoder)

DLE Encoder for Python
======

This encoder provides a simple ASCII transport layer for serial data. It uses 
[the C0 and C1 ASCII control characters](https://en.wikipedia.org/wiki/C0_and_C1_control_codes) for this.
You can find a corresponding C++ implementation
[here](https://egit.irs.uni-stuttgart.de/fsfw/fsfw/src/branch/development/src/fsfw/globalfunctions/DleEncoder.cpp).
This encoder supports two modes:

## Escaped mode

The encoded stream starts with a STX marker and ends with an ETX marker.
STX and ETX occurrences in the stream are escaped and internally encoded as well so the
receiver side can simply check for STX and ETX markers as frame delimiters. When using a
strictly char based reception of packets encoded with DLE,
STX can be used to notify a reader that actual data will start to arrive
while ETX can be used to notify the reader that the data has ended.

Example:

`[0, STX, DLE] -> [STX, 0, 0, DLE, STX + 0x40, DLE, DLE, ETX]`

## Non-escaped mode

The encoded stream starts with DLE STX and ends with DLE ETX. All DLE occurrences in the stream
are escaped with DLE. If the receiver detects a DLE char, it needs to read the next char
to determine whether a start (STX) or end (ETX) of a frame has been detected.

Example:

`[0, STX, DLE] -> [DLE, STX, 0, DLE, STX, DLE, DLE, DLE, ETX]`

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
