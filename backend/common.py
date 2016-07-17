#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import request, response
from functools import wraps
import json
import platform
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
        if res.status_code == 200:
            self.db = res.json()['HostConfig']['Links'][0].split('/')[1].split(':')[0]
            self.enable = True
        else:
            self.enable = False

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
                return False
        return _

    @classmethod
    def create(cls, slack_token):
        endpoint = '/containers/create'
        name = str(uuid4())
        db = str(uuid4())
        redis_payload = {
            'Image': config.DOCKER_REDIS_IMAGE
        }
        hubot_payload = {
            'Image': config.DOCKER_HUBOT_IMAGE,
            'Env': [
                'HUBOT_SLACK_TOKEN={0}'.format(slack_token),
                'HUBOT_CONTAINER_NAME={0}'.format(name + ':' + db)
            ],
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

    @_is_enable
    def update(self, env={}, slack_token=None):
        new_env = self.get_env()
        new_env.update(env)
        if slack_token is not None:
            new_env['HUBOT_SLACK_TOKEN'] = slack_token
        endpoint = '/containers/{0}'.format(self.name)
        requests.delete(
            config.DOCKER_BASEURI + endpoint
        )
        endpoint = '/containers/create'
        self.name = str(uuid4())
        new_env['HUBOT_CONTAINER_NAME'] = self.name + ':' + self.db
        hubot_payload = {
            'Image': 'hubot',
            'Env': self._dict2env(new_env),
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

    @_is_enable
    def get_env(self):
        endpoint = '/containers/{0}/json'.format(self.name)
        res = requests.get(config.DOCKER_BASEURI + endpoint)
        return self._env2dict(res.json()['Config']['Env'])


class User(object):
    def __init__(self, name):
        self.name = name
        redis = Redis(**config.REDIS_INFO)
        self.apikey = reverse_dict(redis.hgetall('apikeys'))[name]
        self.hubots = json.loads(redis.hget('users', name).decode().replace("'", '"'))

    @classmethod
    def create(cls, name):
        redis = Redis(**config.REDIS_INFO)
        apikey = 'hbt-' + str(uuid4())
        res = redis.hsetnx('users', name, [])
        if res:
            redis.hset('apikeys', apikey, name)
            return User(name)
        else:
            return False

    def add_hubot(self, hubot_name):
        self.hubots.append(hubot_name)
        redis = Redis(**config.REDIS_INFO)
        redis.hset('users', self.name, self.hubots)

    def delete_hubot(self, hubot_name):
        self.hubots.remove(hubot_name)
        redis = Redis(**config.REDIS_INFO)
        redis.hset('users', self.name, self.hubots)


class Service(object):
    def __init__(self):
        self.redis = Redis(**config.REDIS_INFO)
        self.users = self.redis.hkeys('users')


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


def RequireNotSatisfiedError(key):
    return failed('Requirements not satisfied', key=key)


def apikey(func):
    @wraps(func)
    def _(*a, **ka):
        redis = Redis(**config.REDIS_INFO)
        apikey = request.params.get('apikey')
        user = redis.hget('apikeys', apikey).decode()
        if apikey is None or user is None:
            return APIKeyNotValidError()
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
        user = redis.hget('apikeys', apikey)
        if apikey is None or user is None and user == 'root':
            return APIKeyNotValidError()
        return func(*a, **ka)
    return _
