#!/usr/bin/env python3

# imports
import sys
import logging.config

import bottle
from bottle import get, post, request, response, template, redirect

import uuid
import requests

# Set up app and logging
app = bottle.default_app()
app.config.load_config('./etc/app.ini')

logging.config.fileConfig(app.config['logging.config'])

KV_URL = app.config['sessions.kv_url'].strip("'")

# Disable Resource warnings produced by Bottle 0.12.19 when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings

    warnings.simplefilter('ignore', ResourceWarning)


@get('/')
def show_form():
    print(KV_URL)
    # session id
    SID = request.get_cookie('SID')
    # check if session ID doesn't exists
    if not SID:
        # create new session id
        SID = uuid.uuid4()
        # set default values
        count1 = 0
        count2 = 0

    # if session id is found
    else:
        # get the session data
        count1 = requests.get(f'{KV_URL}/{SID}').json()[f'{SID}']['count1']
        count2 = requests.get(f'{KV_URL}/{SID}').json()[f'{SID}']['count2']

        # increment count1
        count1 = int(count1) + 1

    # format data
    SDATA = {'count1': count1, 'count2': count2}
    # update into data server with key=SID and value=SDATA
    requests.put(f'{KV_URL}', json={f'{SID}': SDATA})

    # set cookie response header
    response.set_cookie('SID', f'{SID}')

    return template('counter.tpl', counter1=count1, counter2=count2)


@post('/increment')
def increment_count2():
    # session id
    SID = request.get_cookie('SID')
    # check if session ID doesn't exists
    if not SID:
        # create new session id
        SID = uuid.uuid4()
        # set default values
        count1 = 0
        count2 = 0

    # if session ID is found
    else:
        # get the session data
        count1 = requests.get(f'{KV_URL}/{SID}').json()[f'{SID}']['count1']
        count2 = requests.get(f'{KV_URL}/{SID}').json()[f'{SID}']['count2']

        # increment count2
        count2 = int(count2) + 1

    # format data
    SDATA = {'count1': count1, 'count2': count2}
    # update into data server with key=SID and value=SDATA
    requests.put(f'{KV_URL}', json={f'{SID}': SDATA})

    # set cookie response header
    response.set_cookie('SID', f'{SID}')

    return redirect('/')


@post('/reset')
def reset_counts():
    # get session id
    SID = request.get_cookie('SID')

    # delete cookie
    response.delete_cookie('SID')

    # delete the data
    requests.delete(f'{KV_URL}/{SID}')

    return redirect('/')
