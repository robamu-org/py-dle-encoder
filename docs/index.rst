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

Other pages (online)

- `project page on GitHub`_
- This page, when viewed online is at https://tmtccmd.readthedocs.io/en/latest/

.. _`project page on GitHub`: https://github.com/robamu-org/py-dle-encoder

.. toctree::
   :maxdepth: 2
   :caption: Contents:

API Documentation
---------------------

.. automodule:: dle_encoder.dle_encoder
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
