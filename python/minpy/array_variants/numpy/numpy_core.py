#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Definition of grads of core functions"""
from . import numpy_wrapper

import operator
import numpy as np

def register_primitives(reg, make_prim):
    numpy_wrapper.wrap_namespace(np.__dict__, reg, make_prim)

def unbroadcast(ans, x, gradfun):
    """Unbroadcast to original shape.

    :param ans: Data to broadcast.
    :param x: Original data.
    :param gradfun: Gradient function.
    :return: Result with original shape.
    """
    if isinstance(x, np.ndarray):
        shape = x.shape
        def new_fun(g):
            result = gradfun(g)
            while len(shape) < np.ndim(result):
                result = np.sum(result, axis=0)
            for axis, size in enumerate(shape):
                if size == 1:
                    result = np.sum(result, axis=axis, keepdims=True)
            assert np.shape(result) == shape
            return result
    elif isinstance(ans, np.ndarray): # x is numerical value
        new_fun = lambda g: np.sum(gradfun(g))
    else: # both ans and x are numerical value
        return gradfun
    new_fun.__name__ = 'unbroadcast_{0}'.format(gradfun.__name__)
    return new_fun

def gen_sum_grad(ans, x, axis, keepdims):
    xshape = list(x.shape)
    if axis is None:
        return lambda g: np.full(xshape, g)
    if type(axis) is int:
        axis = [axis]
    elif type(axis) is tuple:
        axis = list(axis)
    for a in axis:
        xshape[a] = 1
    def sum_grad(g):
        return np.zeros(x.shape) + g.reshape(tuple(xshape))
    sum_grad.__name__ = 'broadcast {} to {}'.format(x.shape, ans.shape)
    return sum_grad

def def_grads(reg, prims):
    def identity(x):
        return x
    # Dot.
    prims('dot').def_grad(lambda ans, a, b: lambda g: np.dot(g, b.T))
    prims('dot').def_grad(lambda ans, a, b: lambda g: np.dot(a.T, g), argnum=1)

    # Nonlinear functions.
    prims('tanh').def_grad(lambda ans, x: lambda g: g / np.cosh(x) ** 2)
    prims('log').def_grad(lambda ans, x: lambda g: g / x)
    prims('exp').def_grad(lambda ans, x: lambda g: ans * g)

    prims('sum').def_grad(
            lambda ans, x, axis=None, keepdims=False: gen_sum_grad(ans, x, axis, keepdims))
    prims('multiply').def_grad(lambda ans, x, y: unbroadcast(ans, x, lambda g: g * y))
    prims('multiply').def_grad(lambda ans, x, y: unbroadcast(ans, y, lambda g: x * g), argnum=1)
    prims('add').def_grad(lambda ans, x, y: unbroadcast(ans, x, identity))
    prims('add').def_grad(lambda ans, x, y: unbroadcast(ans, y, identity), argnum=1)
    prims('subtract').def_grad(lambda ans, x, y: unbroadcast(ans, x, identity))
    prims('subtract').def_grad(lambda ans, x, y: unbroadcast(ans, y, operator.neg), argnum=1)
    prims('divide').def_grad(lambda ans, x, y: unbroadcast(ans, x, lambda g: g / y))
    prims('divide').def_grad(
            lambda ans, x, y: unbroadcast(ans, y, lambda g: -g * x / y ** 2),
            argnum=1)
    prims('true_divide').def_grad(lambda ans, x, y: unbroadcast(ans, x, lambda g: g / y))
    prims('true_divide').def_grad(
            lambda ans, x, y: unbroadcast(ans, y, lambda g: -g * x / y ** 2),
            argnum=1)
    prims('power').def_grad(lambda ans, x, y: unbroadcast(ans, x, lambda g: g * y * x ** (y - 1)))
    prims('power').def_grad(
            lambda ans, x, y: unbroadcast(ans, y, lambda g: g * np.log(x) * x ** y),
            argnum=1)
    prims('mod').def_grad(lambda ans, x, y: unbroadcast(ans, x, identity))
    prims('mod').def_grad(
            lambda ans, x, y: unbroadcast(ans, y, lambda g: -g * np.floor(x / y)),
            argnum=1)
    prims('negative').def_grad(lambda ans, x: operator.neg)
