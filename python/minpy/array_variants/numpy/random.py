#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Wrapper for NumPy random functions."""
from __future__ import absolute_import

from . import numpy_wrapper
import numpy

def register_primitives(reg, prim_wrapper):
    numpy_wrapper.wrap_namespace(numpy.random.__dict__, reg, prim_wrapper)

def def_grads(reg, prims):
    prims('random').def_grad_zero()
    prims('randn').def_grad_zero()
