#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import redirect, response, request
from datetime import datetime, timedelta
from functools import wraps
from hashlib import sha256
import json
import re
from redis import Redis

with open('config.json', 'r') as f:
    cfg = json.load(f)

redis = Redis(**cfg['REDIS_INFO'])


def session(func):
    @wraps(func)
    def _(*ar, **kw):
        username, session_id = get_session()
        if session_authorize(username, session_id):
            func(*ar, **kw)
        else:
            redirect('/login')
    return _


def logout():
    response.set_cookie(
        'session_id', 'expired',
        expires=datetime.now() - timedelta(1)
    )
    redis.hdel(request.get_cookie('username'), 'session_id')


def _base_authorize(username, key, type_):
    saved = redis.hgetall(username).get(type_)
    key = dynamic_hash(key)
    if saved is not None and saved == key:
        set_session(username)
        return True
    else:
        return False


def session_authorize(username, session_id):
    return _base_authorize(username, session_id, 'session_id')


def password_authorize(username, password):
    return _base_authorize(username, password, 'password')


def get_session():
    return request.get_cookie('username'), request.get_cookie('session_id')


def set_session(username):
    session_id = str(uuid4()).replace('-', '')
    hsh = redis.hgetall(username)
    hsh['session_id'] = session_id
    redis.hmset(username, hsh)
    expire_date = datetime.now() + timedelta(7)
    response.set_cookie('username', username)
    response.set_cookie(
        'session_id', session_id,
        expires=expire_date
    )


def dynamic_hash(value):
    if value is None:
        return ''
    stretch_index = 30
    symbol_score = 4
    symbol_score -= 1 if re.match('[a-z]', value) else 0
    symbol_score -= 1 if re.match('[A-Z]', value) else 0
    symbol_score -= 1 if re.match('[0-9]', value) else 0
    symbol_score -= 1 if re.match('[!#$%&+-*/_@]', value) else 0
    length_score = max(25 - len(value), 0)
    loop = stretch_idx * symbol_score * length_score
    digest = sha256(value).hexdigest()
    for i in range(loop):
        digest = sha256(digest + sha256(i)).hexdigest()
    return digest
