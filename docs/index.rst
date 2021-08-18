.. dle-encoder documentation master file, created by
   sphinx-quickstart on Tue Aug 17 11:27:40 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DLE ASCII encoder for Python
=======================================

This encoder provides a simple ASCII transport layer for serial data.
A give data stream is encoded by adding a STX char at the beginning and an ETX char at the end.
All STX and ETX occurrences in the packet are encoded as well so the receiver can simply look
for STX and ETX occurrences to identify packets.
You can find a C++ implementation
`here <https://egit.irs.uni-stuttgart.de/fsfw/fsfw/src/branch/development/src/fsfw/globalfunctions/DleEncoder.cpp>`_

Escaped mode
---------------------

The encoded stream starts with a STX marker and ends with an ETX marker.
STX and ETX occurrences in the stream are escaped and internally encoded as well so the
receiver side can simply check for STX and ETX markers as frame delimiters. When using a
strictly char based reception of packets encoded with DLE,
STX can be used to notify a reader that actual data will start to arrive
while ETX can be used to notify the reader that the data has ended.

Non-escaped mode
---------------------

The encoded stream starts with DLE STX and ends with DLE ETX. All DLE occurrences in the stream
are escaped with DLE. If the receiver detects a DLE char, it needs to read the next char
to determine whether a start (STX) or end (ETX) of a frame has been detected.

Other pages (online)

- `project page on GitHub`_
- This page, when viewed online is at https://tmtccmd.readthedocs.io/en/latest/

.. _`project page on GitHub`: https://github.com/robamu-org/py-dle-encoder

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Examples
===================

API Documentation
===================

dle_encoder module
---------------------

.. automodule:: dle_encoder.dle_encoder
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
