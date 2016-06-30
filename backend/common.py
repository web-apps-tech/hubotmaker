#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
from uuid import uuid4

import config


class Hubot(object):
    def __init__(self, name, db):
        self.name = name
        self.db = db

    @classmethod
    def create(cls, slack_token):
        endpoint = '/containers/create'
        name = str(uuid4())
        db = str(uuid4())
        redis_payload = {
            'Image': 'redis'
        }
        hubot_payload = {
            'Image': 'hubot',
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
        return cls(name, db)

    def remove(self):
        endpoint = '/containers/{0}'
        self.last_response = requests.delete(
            config.DOCKER_BASEURI + endpoint.format(self.db) + '?force=True'
        )
        if self.last_response.status_code == 204:
            self.last_response = requests.delete(
                config.DOCKER_BASEURI + endpoint.format(self.name) + '?force=True'
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


def RequireNotSatisfiedError(key):
    return failed(key)
