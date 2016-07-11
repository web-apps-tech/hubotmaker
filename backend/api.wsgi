#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, request, response

from common import Hubot, apikey, param, success, failed
import config

app = application = Bottle()
get = app.get
post = app.post
put = app.put
delete = app.delete


@post('/hubot')
@apikey
@param(require=['slack_token'])
def api_create_hubot(params):
    h = Hubot.create(params['slack_token'])
    if h.last_response.status_code in [200, 201]:
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@post('/hubot/start')
@apikey
@param(require=['name'])
def api_start_hubot(params):
    h = Hubot(params['name'])
    h.start()
    if h.last_response.status_code == 204:
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@post('/hubot/stop')
@apikey
@param(require=['name'])
def api_stop_hubot(params):
    h = Hubot(params['name'])
    h.stop()
    if h.last_response.status_code == 204:
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@delete('/hubot')
@apikey
@param(require=['name'])
def api_remove_hubot(params):
    h = Hubot(params['name'])
    h.remove()
    if h.last_response.status_code == 204:
        return success()
    else:
        return failed(error=h.last_response.text)


@put('/hubot')
@apikey
@param(require=['name'])
def api_update_hubot(params):
    h = Hubot(params['name'])
    h.stop()
    h.update()
    if h.last_response.status_code in [200, 201]:
        h.start()
        if h.last_response.status_code == 204:
            return success(h.name)
    return failed(error=h.last_response.text)


@get('/hubot/<name>/env')
def api_get_hubot_env(name):
    h = Hubot(name)
    if h.enable:
        return success(h.get_env())
    return failed()

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
