#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import request, response
from functools import wraps
from hashlib import sha512 as enhash
import json
import pymysql as DB
from pymysql.cursors import DictCursor as DC
import platform
import re
from redis import Redis
import requests
from uuid import uuid4

import config


class Hubot(object):
    def __init__(self, name, res=None):
        endpoint = '/containers/{0}/json'
        self.name = name
        res = requests.get(
            config.DOCKER_BASEURI + endpoint.format(self.name)
        )
        if res is not None:
            self.last_response = res
        if res and res.status_code == 200:
            self.db = res.json()['HostConfig']['Links'][0].split('/')[1].split(':')[0]
            self.enable = True
        else:
            self.enable = False
            raise Exception('CANNOT FIND THE HUBOT')

    def _env2dict(self, env):
        return {k: v for k, v in [item.split('=') for item in env]}

    def _dict2env(self, dic):
        PY_VER = platform.python_version_tuple()
        if PY_VER[0] == '2':
            return [k + '=' + str(v) for k, v in dic.iteritems()]
        elif PY_VER[0] == '3':
            return [k + '=' + str(v) for k, v in dic.items()]
        else:
            raise Exception('PY_VER IS UNKNOWN: {}'.format(PY_VER[0]))

    def _is_enable(func):
        @wraps(func)
        def _(self, *a, **ka):
            if self.enable:
                return func(self, *a, **ka)
            else:
                raise Exception('CANNOT FIND THE HUBOT')
        return _

    @classmethod
    def create(cls, slack_token, script_env=None):
        endpoint = '/containers/create'
        name = str(uuid4())
        db = str(uuid4())
        if isinstance(script_env, list):
            script_env = ["{0}=1".format(e) for e in script_env]
        elif isinstance(script_env, str):
            script_env = ["{0}=1".format(e) for e in json.loads(script_env)]
        else:
            script_env = []
        redis_payload = {
            'Image': config.DOCKER_REDIS_IMAGE
        }
        hubot_payload = {
            'Image': config.DOCKER_HUBOT_IMAGE,
            'Env': [
                'HUBOT_SLACK_TOKEN={0}'.format(slack_token),
                'HUBOT_CONTAINER_NAME={0}'.format(name + ':' + db)
            ] + script_env,
            'HostConfig': {
                'Links': [db + ":db"]
            }
        }
        lres = requests.post(
            config.DOCKER_BASEURI + endpoint + '?name={}'.format(db),
            headers={
                'Content-type': 'application/json'
            },
            data=json.dumps(redis_payload)
        )
        if lres.status_code == 201:
            lres = requests.post(
                config.DOCKER_BASEURI + endpoint + '?name={}'.format(name),
                headers={
                    'Content-type': 'application/json'
                },
                data=json.dumps(hubot_payload)
            )
        return cls(name, lres)

    @_is_enable
    def remove(self):
        endpoint = '/containers/{0}'
        self.last_response = requests.delete(
            config.DOCKER_BASEURI + endpoint.format(self.name)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.delete(
                config.DOCKER_BASEURI + endpoint.format(self.db)
            )
            return True
        return False

    @_is_enable
    def start(self):
        endpoint = '/containers/{0}/start'
        self.last_response = requests.post(
            config.DOCKER_BASEURI + endpoint.format(self.db)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.post(
                config.DOCKER_BASEURI + endpoint.format(self.name)
            )
            return True
        return False

    @_is_enable
    def stop(self):
        endpoint = '/containers/{0}/stop'
        self.last_response = requests.post(
            config.DOCKER_BASEURI + endpoint.format(self.db)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.post(
                config.DOCKER_BASEURI + endpoint.format(self.name)
            )
            return True
        return False

    @_is_enable
    def restart(self):
        endpoint = '/containers/{0}/restart'
        self.last_response = requests.post(
            config.DOCKER_BASEURI + endpoint.format(self.db)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.post(
                config.DOCKER_BASEURI + endpoint.format(self.name)
            )
            return True
        return False

    @_is_enable
    def update(self, env={}, slack_token=None, script_env=None):
        if isinstance(script_env, list):
            script_env = ["{0}=1".format(e) for e in script_env]
        elif isinstance(script_env, str):
            try:
                script_env = ["{0}=1".format(e) for e in json.loads(script_env)]
            except:
                raise Exception('JSON NOT VALID: script_env')
        else:
            script_env = []
        old_env = self.get_env()
        new_env = env
        if slack_token is not None:
            new_env['HUBOT_SLACK_TOKEN'] = slack_token
        else:
            new_env['HUBOT_SLACK_TOKEN'] = old_env['HUBOT_SLACK_TOKEN']
        endpoint = '/containers/{0}'.format(self.name)
        requests.delete(
            config.DOCKER_BASEURI + endpoint
        )
        endpoint = '/containers/create'
        new_env['HUBOT_CONTAINER_NAME'] = self.name + ':' + self.db
        hubot_payload = {
            'Image': 'hubot',
            'Env': self._dict2env(new_env) + script_env,
            'HostConfig': {
                'Links': [self.db + ":db"]
            }
        }
        self.last_response = requests.post(
            config.DOCKER_BASEURI + endpoint + '?name={}'.format(self.name),
            headers={
                'Content-type': 'application/json'
            },
            data=json.dumps(hubot_payload)
        )
        return True

    @_is_enable
    def get_env(self):
        endpoint = '/containers/{0}/json'.format(self.name)
        res = requests.get(config.DOCKER_BASEURI + endpoint)
        return self._env2dict(res.json()['Config']['Env'])

    @_is_enable
    def get_status(self):
        endpoint = '/containers/{}/json'
        self.last_response = requests.get(
            config.DOCKER_BASEURI + endpoint.format(self.name)
        )
        return json.loads(self.last_response.text)['State']['Status']


class User(object):
    def __init__(self, name):
        self.name = name
        self.apikey = self._get_apikey()
        self.hubots = self._get_hubot_list()
        self.is_active = self._is_active()

    @classmethod
    def create(cls, name, password):
        query = 'INSERT INTO users (username, password) VALUES (%s, %s);'
        with DB.connect(**config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (name, enhash(password.encode()).hexdigest())
                )
            except:
                return None
        return cls(name)

    def remove(self):
        for hubot_name in self.hubots:
            h = Hubot(hubot_name)
            h.stop()
            h.remove()
            self.delete_hubot(hubot_name)
        redis = Redis(**config.REDIS_INFO)
        redis.delete(self.apikey)
        query = 'DELETE FROM users \
        WHERE username=%s;'
        with DB.connect(**config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (self.name, )
                )
            except:
                return False
        return True

    def activate(self, password):
        query = 'UPDATE users \
        SET activate=1 \
        WHERE username=%s AND password=%s;'
        with DB.connect(**config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (self.name, enhash(password.encode()).hexdigest())
                )
            except:
                return False
        return True

    def generate_apikey(self):
        redis = Redis(**config.REDIS_INFO)
        apikey = 'hbt-' + str(uuid4())
        redis.setex(apikey, self.name, config.APIKEY_TTL * 60 * 60)
        self.apikey = apikey
        return apikey

    def _is_active(self):
        query = 'SELECT activate FROM users WHERE username=%s;'
        with DB.connect(cursorclass=DC, **config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (self.name, )
                )
                row = cursor.fetchone()
            except:
                return False
        return bool(row['activate'])

    def _get_hubot_list(self):
        query = 'SELECT hubotname FROM hubots WHERE username=%s;'
        with DB.connect(cursorclass=DC, **config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (self.name,)
                )
                rows = cursor.fetchall()
            except:
                return False
        return [row['hubotname'] for row in rows]

    def _get_apikey(self):
        redis = Redis(**config.REDIS_INFO)
        for apikey in redis.keys('*'):
            owner = redis.get(apikey).decode()
            if self.name == owner:
                return apikey
        return None

    def add_hubot(self, hubot_name):
        query = 'INSERT INTO hubots VALUES (%s, %s);'
        with DB.connect(**config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (self.name, hubot_name)
                )
            except:
                return False
        self.hubots.append(hubot_name)
        return True

    def delete_hubot(self, hubot_name):
        query = 'DELETE FROM hubots WHERE username=%s AND hubotname=%s;'
        with DB.connect(**config.MySQL) as cursor:
            try:
                cursor.execute(
                    query,
                    (self.name, hubot_name)
                )
            except:
                return False
        self.hubots.remove(hubot_name)
        return True


class Service(object):
    def __init__(self):
        self.redis = Redis(**config.REDIS_INFO)
        self.users = self._get_userlist()
        self.available_scripts = self._get_hubot_scripts()

    def _get_userlist(self):
        query = 'SELECT username FROM users'
        with DB.connect(cursorclass=DC, **config.MySQL) as cursor:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
            except:
                return None
        return [row['username'] for row in rows]

    def _get_hubot_scripts(self):
        available = []
        regex = re.compile('^\$\{(.+):\+.+\}$')
        with open('Docker/hubot/hubot', 'r') as f:
            for row in f:
                if regex.match(row):
                    available.append(regex.findall(row)[0])
        available.remove('HOGE')
        return available


def failed(msg='Failed', **ka):
    return json.dumps(dict(
        status=False,
        message=msg,
        **ka
    )) + '\n'


def success(msg='Succeeded', **ka):
    return json.dumps(dict(
        status=True,
        message=msg,
        **ka
    )) + '\n'


def APIKeyNotValidError():
    return failed('API key not valid')


def NotPermittedError():
    return failed('You are not permitted.')


def RequireNotSatisfiedError(key):
    return failed('Requirements not satisfied', key=key)


def AuthenticationError():
    return failed('Auth Error')


def apikey(func):
    @wraps(func)
    def _(*a, **ka):
        redis = Redis(**config.REDIS_INFO)
        apikey = request.params.get('apikey')
        user = redis.get(apikey)
        if apikey is None or user is None:
            return APIKeyNotValidError()
        return func(user=user.decode(), *a, **ka)
    return _


def password(func):
    @wraps(func)
    def _(*a, **ka):
        user = request.params.get('username')
        password = request.params.get('password')
        if user is None or password is None:
            return AuthenticationError()
        with DB.connect(cursorclass=DC, **config.MySQL) as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE username=%s;',
                user
            )
            row = cursor.fetchone()
        if row['password'] != enhash(password.encode()).hexdigest():
            return AuthenticationError()
        return func(user=user, *a, **ka)
    return _


def param(require=[], option=[]):
    def wrapper(func):
        @wraps(func)
        def _(*a, **ka):
            params = {}
            form_data = request.forms
            for key in require:
                if key not in form_data:
                    response.status = 400
                    return RequireNotSatisfiedError(key)
                else:
                    params[key] = form_data[key]
            for key in option:
                if key in form_data:
                    params[key] = form_data[key]
            return func(params=params, *a, **ka)
        return _
    return wrapper


def query(require=[], option=[]):
    def wrapper(func):
        @wraps(func)
        def _(*a, **ka):
            query = {}
            form_data = request.query
            for key in require:
                if key not in form_data:
                    response.status = 400
                    return RequireNotSatisfiedError(key)
                else:
                    query[key] = form_data[key]
            for key in option:
                if key in form_data:
                    query[key] = form_data[key]
            return func(query=query, *a, **ka)
        return _
    return wrapper


def reverse_dict(dic):
    PY_VER = platform.python_version_tuple()
    if PY_VER[0] == '2':
        return {v: k for k, v in dic.iteritems()}
    elif PY_VER[0] == '3':
        return {v: k for k, v in dic.items()}


def decode_bytesdict(dic):
    PY_VER = platform.python_version_tuple()
    if PY_VER[0] == '3':
        return {k.decode(): v.decode() for k, v in dic.items()}
    return dic


def root(func):
    @wraps(func)
    def _(*a, **ka):
        redis = Redis(**config.REDIS_INFO)
        apikey = request.params.get('apikey')
        user = redis.get(apikey)
        if apikey is None or user is None:
            return APIKeyNotValidError()
        with DB.connect(cursorclass=DC, **config.MySQL) as cursor:
            cursor.execute(
                'SELECT isadmin FROM users WHERE username=%s;',
                user
            )
            row = cursor.fetchone()
            if not row['isadmin']:
                return NotPermittedError()
        return func(user=user, *a, **ka)
    return _
