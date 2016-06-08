#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, HTTPResponse, redirect, response, request
from bottle import jinja2_view as view
import json

import api
import auth

with open('config.json', 'r') as f:
    cfg = json.load(f)

app = application = Bottle()
route = get = app.get
post = app.post

app.mount('/api', api.app)


@route('/')
@view('index.tpl')
def index():
    return {}


@route('/signup')
@view('signup.tpl')
def signup():
    return {}


@route('/register')
@view('register.tpl')
def register():
    return {}


@route('/login')
@view('login.tpl')
def login():
    username, session_id = auth.get_session()
    if auth.session_authorize(username, session_id):
        redirect('/user')
    return {}


@post('/login')
def login(goto):
    username = request.forms.get('username')
    password = request.forms.get('password')
    if auth.password_authorize(username, password):
        redirect('/user')
    else:
        redirect('/')


@route('/user')
@view('user.tpl')
@auth.session
def user():
    username, _ = auth.get_session()
    return {}


@route('/user/hubot/add')
@view('hubot_add.tpl')
@auth.session
def hubot_add():
    return {}


@route('/user/hubot/modify/<hubot_id>')
@view('hubot_mod.tpl')
@auth.session
def hubot_mod(hubot_id):
    return {}


@route('/logout')
def logout():
    auth.logout()
    redirect('/')

if __name__ == '__main__':
    app.run()
