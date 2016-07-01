#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import request, response
from functools import wraps
import json
import requests
from uuid import uuid4

import config


class Hubot(object):
    def __init__(self, name):
        endpoint = '/containers/{0}/json'
        self.name = name
        res = requests.get(
            config.DOCKER_BASEURI + endpoint.format(self.name)
        )
        self.db = res.json()['HostConfig']['Links'][0].split('/')[1].split(':')[0]

    def _env2dict(env):
        return {k: v for k, v in [item.split('=') for item in env]}

    def _dict2env(dic):
        return [k + '=' + str(v) for k, v in dic.iteritems()]

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
                'HUBOT_SLACK_TOKEN={0}'.format(slack_token)
            ],
            'HostConfig': {
                'Links': [db + ":db"]
            }
        }
        requests.post(
            config.DOCKER_BASEURI + endpoint + '?name={}'.format(db),
            headers={
                'Content-type': 'application/json'
            },
            data=json.dumps(redis_payload)
        )
        requests.post(
            config.DOCKER_BASEURI + endpoint + '?name={}'.format(name),
            headers={
                'Content-type': 'application/json'
            },
            data=json.dumps(hubot_payload)
        )
        return cls(name)

    def remove(self):
        endpoint = '/containers/{0}'
        self.last_response = requests.delete(
            config.DOCKER_BASEURI + endpoint.format(self.name)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.delete(
                config.DOCKER_BASEURI + endpoint.format(self.db)
            )

    def start(self):
        endpoint = '/containers/{0}/start'
        self.last_response = requests.post(
            config.DOCKER_BASEURI + endpoint.format(self.db)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.post(
                config.DOCKER_BASEURI + endpoint.format(self.name)
            )

    def stop(self):
        endpoint = '/containers/{0}/stop'
        self.last_response = requests.post(
            config.DOCKER_BASEURI + endpoint.format(self.db)
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.post(
                config.DOCKER_BASEURI + endpoint.format(self.name)
            )

    def update(self, env={}, slack_token=None):
        endpoint = '/containers/{0}/json'.format(self.name)
        if slack_token is None:
            res = request.get(config.DOCKER_BASEURI + endpoint)
            new_env = _env2dict(res.json()['Config']['Env'])
            new_env.update(env)
        endpoint = '/containers/{0}'.format(self.name)
        requests.delete(
            config.DOCKER_BASEURI + endpoint + '?force=True'
        )
        endpoint = '/containers/create'
        self.name = str(uuid4())
        hubot_payload = {
            'Image': 'hubot',
            'Env': _dict2env(new_env.iteritems()),
            'HostConfig': {
                'Links': [self.db + ":db"]
            }
        }
        self.last_response = requrests.post(
            config.DOCKER_BASEURI + endpoint,
            headers={
                'Content-type': 'application/json'
            },
            data=hubot_payload
        )

    def get_env(self):
        endpoint = '/containers/{0}/json'.format(self.name)
        res = requests.get(config.DOCKER_BASEURI + endpoint)
        return _env2dict(res.json()['Config']['Env'])


def failed(msg='Failed'):
    return {
        'status': False,
        'message': msg
    }


def success(msg='Succeeded'):
    return {
        'status': True,
        'message': msg
    }


def APIKeyNotValidError():
    return failed('API key not valid')


def RequireNotSatisfiedError(key):
    return failed(key)


def apikey(func):
    @wraps(func)
    def _(*a, **ka):
        if request.forms.get('apikey') == config.APIKEY:
            return func(*a, **ka)
        else:
            return APIKeyNotValidError()
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
