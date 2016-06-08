#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, HTTPResponse, request
import json
from redis import Redis

with open('config.json', 'r') as f:
    cfg = json.load(f)

redis = Redis(**cfg['REDIS_INFO'])

app = application = Bottle()
get = app.get
post = app.post
put = app.put
delete = app.delete


class RequireNotSatisfiedError(Exception):
    pass


def _require(keys):
    params = {}
    for key in keys:
        value = request.forms.get(key)
        if value is not None:
            params[key] = value
        else:
            raise RequireNotSatisfiedError(key)
    return params


@post('/user')
def api_user_post(id_):
    required_params = ['username', 'password']
    params = _require()


@get('/user/<id_:int>')
def api_user_get(id_):
    pass


@put('/user/<id_:int>')
def api_user_put(id_):
    pass


def register():
    pass
