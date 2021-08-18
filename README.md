[![Documentation Status](https://readthedocs.org/projects/dle-encoder/badge/?version=latest)](https://dle-encoder.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/robamu-org/py-dle-encoder/branch/main/graph/badge.svg?token=GQ5VW8PKKS)](https://codecov.io/gh/robamu-org/py-dle-encoder)

DLE Encoder for Python
======

This encoder provides a simple ASCII transport layer for serial data.
A give data stream is encoded by adding a STX (0x02) char at the beginning and an ETX (0x03) char at the end.
All STX and ETX occurrences in the packet are encoded as well so the receiver can simply look for STX and ETX
occurrences to identify packets.

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

test_stream = bytearray([1, 2, 3])
encoded_stream = dle_encoder.encode(test_stream)
print(test_stream)

decode_status, decoded_stream, decoded_bytes = dle_encoder.decode(encoded_stream)
print(decoded_stream)
```
