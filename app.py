#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import request
from welcome import welcome_action
from schedule import schedule_action
from sponsors import sponsors_action
from tracks import tracks_action
# Flask app should start in global layout
app = Flask(__name__)
log = app.logger

actions = {
    'welcome': welcome_action,
    'schedule': schedule_action,
    'sponsors': sponsors_action,
    'tracks': tracks_action
}

@app.route('/status', methods=['GET'])
def status():
    return 'OK'

@app.route('/static_reply', methods=['POST'])
def static_reply():
    global actions
    req = request.get_json(silent=True, force=True)
    print(req)
    try:
        action = req['queryResult']['action']
    except AttributeError:
        return 'json error'
    if action in actions:
        functor = actions[action]
        if functor.__doc__:
            print(functor.__doc__.split('\n')[0])
        response = functor(req)
    else:
        log.error('action unable')
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 50000))
    print("App running in port %d" % port)
    app.run(debug=True, port=port, host='127.0.0.1')