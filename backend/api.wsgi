#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle

from common import Hubot, User, Service, apikey, password, param, success, failed, root

app = application = Bottle()
get = app.get
post = app.post
put = app.put
delete = app.delete


@get('/admin/hubot/available_scripts')
@root
def api_admin_available_scripts(user):
    s = Service()
    return success(s.available_scripts)


@post('/admin/hubot/restartall')
@root
def api_admin_restart_all(user):
    s = Service()
    for user in s.users:
        u = User(user)
        for hubot in u.hubots:
            h = Hubot(hubot)
            if h.get_status() == 'running':
                h.restart()
                if not h.last_response.status_code == 204:
                    return failed(h.last_response.text)
    return success()


@post('/user')
@param(require=['username', 'password'])
def api_create_user(params):
    u = User.create(params['username'], params['password'])
    if u:
        return success()
    else:
        return failed()


@put('/user/activate')
@param(require=['username', 'password'])
def api_activate_user(params):
    u = User(params['username'])
    if u.activate(params['password']):
        return success()
    else:
        return failed()


@post('/user/apikey')
@password
def api_generate_apikey(user):
    u = User(user)
    if u.is_active:
        apikey = u.generate_apikey()
        return success(apikey=apikey)
    else:
        return failed('The user has not been activated')


@get('/user/hubot/list')
@apikey
def api_get_hubot_list(user):
    u = User(user)
    return success(u.hubots)


@delete('/user')
@root
@param(require=['username'])
def api_delete_user(params, user):
    u = User(params['username'])
    if u.remove():
        return success()
    else:
        return failed()


@post('/hubot')
@apikey
@param(require=['slack_token'], option=['script_env'])
def api_create_hubot(params, user):
    u = User(user)
    h = Hubot.create(
        slack_token=params['slack_token'],
        script_env=params.get('script_env')
    )
    if h.last_response.status_code in [200, 201]:
        u.add_hubot(h.name)
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@post('/hubot/start')
@apikey
@param(require=['name'])
def api_start_hubot(params, user):
    h = Hubot(params['name'])
    h.start()
    if h.last_response.status_code == 204:
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@post('/hubot/stop')
@apikey
@param(require=['name'])
def api_stop_hubot(params, user):
    h = Hubot(params['name'])
    h.stop()
    if h.last_response.status_code == 204:
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@post('/hubot/restart')
@apikey
@param(require=['name'])
def api_restart_hubot(params, user):
    h = Hubot(params['name'])
    h.restart()
    if h.last_response.status_code == 204:
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@delete('/hubot')
@apikey
@param(require=['name'])
def api_remove_hubot(params, user):
    u = User(user)
    h = Hubot(params['name'])
    h.remove()
    if h.last_response.status_code == 204:
        u.delete_hubot(h.name)
        return success()
    else:
        return failed(error=h.last_response.text)


@put('/hubot')
@apikey
@param(require=['name'], option=['slack_token', 'script_env'])
def api_update_hubot(params, user):
    options = {k: v for k, v in params.items() if k != 'name'}
    h = Hubot(params['name'])
    h.stop()
    if not h.update(**options):
        return failed(error='json not valid: script_env')
    if h.last_response.status_code in [200, 201]:
        h.start()
        if h.last_response.status_code == 204:
            return success()
    return failed(error=h.last_response.text)


@get('/hubot/<name>/status')
def api_get_hubot_status(name):
    h = Hubot(name)
    if h.enable:
        return success(h.get_status())
    return failed(error='No Such Container: {}'.format(name))


@get('/hubot/<name>/env')
def api_get_hubot_env(name):
    h = Hubot(name)
    if h.enable:
        return success(h.get_env())
    return failed(error='No Such Container: {}'.format(name))


@get('/hubot/<name>/db')
def api_get_hubot_db(name):
    h = Hubot(name)
    if h.enable:
        return success(h.db)
    return failed(error='No Such Container: {}'.format(name))

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
