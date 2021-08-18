.. dle-encoder documentation master file, created by
   sphinx-quickstart on Tue Aug 17 11:27:40 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DLE ASCII encoder for Python
=======================================

This encoder provides a simple ASCII transport layer for serial data. It uses 
[the C0 and C1 ASCII control characters](https://en.wikipedia.org/wiki/C0_and_C1_control_codes) for this.
You can find a corresponding C++ implementation
` here <https://egit.irs.uni-stuttgart.de/fsfw/fsfw/src/branch/development/src/fsfw/globalfunctions/DleEncoder.cpp>`_.
This encoder supports two modes:

Escaped mode
---------------------

The encoded stream starts with a STX marker and ends with an ETX marker.
STX and ETX occurrences in the stream are escaped and internally encoded as well so the
receiver side can simply check for STX and ETX markers as frame delimiters. When using a
strictly char based reception of packets encoded with DLE,
STX can be used to notify a reader that actual data will start to arrive
while ETX can be used to notify the reader that the data has ended.

Example:

``[0, STX, DLE] -> [STX, 0, 0, DLE, STX + 0x40, DLE, DLE, ETX]``

Non-escaped mode
---------------------

The encoded stream starts with DLE STX and ends with DLE ETX. All DLE occurrences in the stream
are escaped with DLE. If the receiver detects a DLE char, it needs to read the next char
to determine whether a start (STX) or end (ETX) of a frame has been detected.

Example:

``[0, STX, DLE] -> [DLE, STX, 0, DLE, STX, DLE, DLE, DLE, ETX]``

Other pages (online)

- `project page on GitHub`_
- This page, when viewed online is at https://tmtccmd.readthedocs.io/en/latest/

.. _`project page on GitHub`: https://github.com/robamu-org/py-dle-encoder

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Examples
===================

Here is an example on how to use the escaped mode

::

    import dle_encoder

    encoder = dle_encoder.DleEncoder()
    test_array = bytearray([1, 2, 3])
    encoded = encoder.encode(test_array)
    retval, decoded, bytes_decoded = encoder.decode(encoded)

    print(test_array)
    print(encoded)
    print(decoded)

The non-escaped mode can be used by passing ``escape_stx_etc=False`` to the
:py:class:`dle_encoder.dle_encoder.DleEncoder` constructor.

API Documentation
===================

dle_encoder module
---------------------

.. automodule:: dle_encoder.dle_encoder
   :members:
   :undoc-members:
   :show-inheritance:

DleEncoder class
---------------------

.. autoclass:: dle_encoder.dle_encoder.DleEncoder
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
