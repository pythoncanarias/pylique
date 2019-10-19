#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from flask import make_response


def parse_response(result: object) -> object:
    """parse response in json format for sending to the client side"""
    res = json.dumps(result)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
