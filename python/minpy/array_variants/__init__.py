#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import enum

from ..utils import common
from . import numpy
from . import mxnet

class ArrayType(enum.Enum):
    """Enumeration of types of arrays."""
    NUMPY = 0
    MXNET = 1

variants = {
        'numpy': ArrayType.NUMPY,
        'mxnet': ArrayType.MXNET
        }

array_types = {
        'numpy': numpy.array_type,
        'mxnet': mxnet.array_type,
}
number_types = {
        'native': [int, float],
        'numpy': numpy.number_type,
        'mxnet': mxnet.number_type,
}
