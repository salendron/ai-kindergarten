#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO
"""
__author__ = 'Bruno Hautzenberger'

import bottle
from .webhandler import index

def setup_routing():
    bottle.route('/', ['GET', 'POST'], index)
