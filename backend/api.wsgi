#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle

from common import Hubot, Note, User, Service, apikey, password, param, success, failed, root

app = application = Bottle()
get = app.get
post = app.post
put = app.put
delete = app.delete


@get('/available_scripts')
def api_available_scripts():
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

@delete('/user')
@root
@param(require=['username'])
def api_delete_user(params, user):
    u = User(params['username'])
    if u.remove():
        return success()
    else:
        return failed()


@get('/user')
@apikey
def api_get_username(user):
    return success(user)


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


@get('/user/apikey')
@password
def api_get_apikey(user):
    u = User(user)
    if u.is_active:
        apikey = u.apikey
        if apikey:
            return success(apikey=apikey)
        return failed('apikey has not been generated.')
    return failed('user has not been activated.')


@get('/user/hubot/list')
@apikey
def api_get_hubot_list(user):
    u = User(user)
    return success(u.hubots)


@post('/hubot')
@apikey
@param(require=['slack_token'], option=['script_env'])
def api_create_hubot(params, user):
    u = User(user)
    try:
        h = Hubot.create(
            slack_token=params['slack_token'],
            script_env=params.get('script_env')
        )
    except Exception as err:
        return failed(error=str(err))
    if h.last_response.status_code in [200, 201]:
        u.add_hubot(h.name)
        return success(name=h.name)
    else:
        return failed(error=h.last_response.text)


@post('/hubot/<name>/start')
@apikey
def api_start_hubot(name, user):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    h.start()
    if h.last_response.status_code == 204:
        return success()
    elif h.last_response.status_code == 304:
        return failed(error="Given hubot already started")
    else:
        return failed(error=h.last_response.text)


@post('/hubot/<name>/stop')
@apikey
def api_stop_hubot(name, user):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    h.stop()
    if h.last_response.status_code == 204:
        return success()
    elif h.last_response.status_code == 304:
        return failed(error="Given hubot already stopped")
    else:
        return failed(error=h.last_response.text)


@post('/hubot/<name>/restart')
@apikey
def api_restart_hubot(name, user):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    h.restart()
    if h.last_response.status_code == 204:
        return success()
    else:
        return failed(error=h.last_response.text)


@delete('/hubot/<name>')
@apikey
def api_remove_hubot(name, user):
    u = User(user)
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    h.remove()
    if h.last_response.status_code == 204:
        u.delete_hubot(name)
        return success()
    else:
        return failed(error=h.last_response.text)


@put('/hubot/<name>')
@apikey
@param(option=['slack_token', 'script_env'])
def api_update_hubot(params, name, user):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    h.stop()
    h.update(**params)
    if h.last_response.status_code in [200, 201]:
        h.start()
        if h.last_response.status_code == 204:
            return success()
    return failed(error=h.last_response.text)


@get('/hubot/<name>/status')
def api_get_hubot_status(name):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    if h.enable:
        return success(
            True if h.get_status() == 'running' else False
        )
    return failed(error='No Such Container: {}'.format(name))


@get('/hubot/<name>/env')
@apikey
def api_get_hubot_env(name, user):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    if h.enable:
        return success(h.get_env())
    return failed(error='No Such Container: {}'.format(name))


@get('/hubot/<name>/db')
def api_get_hubot_db(name):
    try:
        h = Hubot(name)
    except Exception as err:
        return failed(error=str(err))
    if h.enable:
        return success(h.db)
    return failed(error='No Such Container: {}'.format(name))


@post('/hubot/<name>/note')
@apikey
@param(require=['text'])
def api_post_hubot_note(params, name):
    h = Hubot(name)
    if h.enable:
        n = Note(name)
        try:
            n.set(params['text'])
        except Exception as err:
            return failed(error=str(err))
        return success()
    return failed(error='No such Hubot')


@get('/hubot/<name>/note')
@apikey
def api_get_hubot_note(name):
    h = Hubot(name)
    if h.enable:
        n = Note(name)
        text = n.get()
        if text is not None:
            return success(text)
        return failed(error='note get error')
    return failed(error='No such Hubot')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
