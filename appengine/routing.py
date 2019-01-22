#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The xamoom main API router
Copyright (c) 2018, xamoom GmbH.
"""
__author__ = 'Bruno Hautzenberger'

import bottle
from bottle import static_file

from tictactoe.routing import setup_routing as setup_tictactoe


def serve_css(filepath):
    return static_file(filepath, root="static/web/css")


def serve_img(filepath):
    return static_file(filepath, root="static/web/img")


def setup_routing():
    setup_tictactoe()

    # Static Routes
    bottle.route("/css/<filepath:re:.*\.css>", ['GET'], serve_css)
    bottle.route("/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>", ['GET'], serve_img)

    """
    @get("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
    def font(filepath):
        return static_file(filepath, root="static/font")

    @get("/static/js/<filepath:re:.*\.js>")
    def js(filepath):
        return static_file(filepath, root="static/js")
    """
