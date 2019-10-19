#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from parse_response import parse_response


def get_event_information() -> object:
    url = 'https://pythoncanarias.es/api/v1/events/pydaygc19/'
    response = requests.get(url)
    data = response.json()
    return data


def welcome_action(req: object = None) -> object:
    """welcome action
    """
    event_information = get_event_information()
    result = {
        "fulfillmentMessages": [
            {
                "payload": {
                    "telegram": {
                        "text": f"Hola, bienvenido. \n{event_information['result']['description']}",
                        "parse_mode": "Markdown"
                    }
                },
                "platform": "TELEGRAM",
            },
        ],
    }
    response = parse_response(result)
    return response
