#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, request, response

from common import Hubot, apikey, param, success, failed
import config

app = application = Bottle()
get = app.get
post = app.post

@post('/hubot/run')
@apikey
@param(require=['slack_token'])
def api_run_hubot(params):
    h = Hubot.create(params['slack_token'])
    h.start()
        return success()
    if h.last_response.status_code == 204:
    else:
        return failed()
