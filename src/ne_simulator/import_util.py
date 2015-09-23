# -*- coding: utf-8 -*-
from importlib import import_module


def import_obj(object_from_package):
    elements = object_from_package.split('.')
    if len(elements) < 2:
        raise RuntimeError(
            'Can not auto import {}'.format(object_from_package))
    obj = elements[-1]
    package = ".".join(elements[:-1])
    return getattr(import_module(package), obj)
