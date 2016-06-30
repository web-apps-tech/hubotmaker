#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, request, response

from common import Hubot, apikey, param, success, failed
import config

app = application = Bottle()
get = app.get
post = app.post

@post('/')
@apikey
@param(require=['slack_token'])
def api_run_hubot(params):
    h = Hubot.create(params['slack_token'])
    h.start()
    if h.last_status == 204:
        return success()
    else:
        return failed()
