#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO
"""
__author__ = 'Bruno Hautzenberger'

import bottle
from routing import setup_routing
from config import ENV

setup_routing()

app = bottle.app()


# FORCE SSL
def redirect_http_to_https(callback):
    def wrapper(*args, **kwargs):
        scheme = bottle.request.urlparts[0]
        if scheme == 'http':
            # request is http; redirect to https
            bottle.redirect(bottle.request.url.replace('http', 'https', 1))
        else:
            # request is already https; okay to proceed
            return callback(*args, **kwargs)
    return wrapper


# ON GCP this starts automatically via gunicorn
if ENV == "LOCAL":
    bottle.run(host='0.0.0.0')
else:
    # force ssl only on gae
    bottle.install(redirect_http_to_https)
