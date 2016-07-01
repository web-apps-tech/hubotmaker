#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, request, response

from common import Hubot, apikey, param, success, failed
import config

app = application = Bottle()
get = app.get
post = app.post
delete = app.delete

@post('/hubot')
@apikey
@param(require=['slack_token'])
def api_run_hubot(params):
    h = Hubot.create(params['slack_token'])
    if h.last_response.status_code == 204:
        return success(h.name)
    else:
        return failed(h.name)


@post('/hubot/start')
@apikey
@param(require=['name'])
def api_start_hubot(params):
    h = Hubot(params['name'])
    h.start()
    if h.last_response.status_code == 204:
        return success(h.name)
    else:
        return success(h.name)


@post('/hubot/stop')
@apikey
@param(require=['name'])
def api_stop_hubot(params):
    h = Hubot(params['name'])
    h.stop()
    if h.last_response.status_code == 204:
        return success(h.name)
    else:
        return failed(h.name)


@delete('/hubot')
@apikey
@param(require=['name'])
def api_remove_hubot(params):
    h = Hubot(params['name'])
    h.remove()
    if h.last_response.status_code == 204:
        return success()
    else:
        return failed()


@get('/hubot/<name>/env')
def api_get_hubot_env(name):
    h = Hubot(name)
    return success(h.get_env())
