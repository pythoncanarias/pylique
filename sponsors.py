#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from parse_response import parse_response
BASE_URL = 'https://pythoncanarias.es'


def get_sponsors_information() -> object:
    url = 'https://pythoncanarias.es/api/v1/events/pydaygc19/sponsors'
    response = requests.get(url)
    data = response.json()
    return data


def create_sponsor_cards(sponsor_information: list) -> list:
    sponsors = []
    for sponsor in sponsor_information['result']:
        sponsors.append(
            {
                "card": {
                    "title": sponsor['name'],
                    "imageUri": BASE_URL + sponsor['logo']
                },
                'platform': 'TELEGRAM',
            }
        )
    return sponsors


def sponsors_action(req: object = None) -> object:
    """sponsor action
    """
    sponsors_information = get_sponsors_information()
    sponsor_cards = create_sponsor_cards(sponsors_information)
    result = {"fulfillmentMessages": []}
    for sponsor_card in sponsor_cards:
        result['fulfillmentMessages'].append(sponsor_card)
    response = parse_response(result)
    return response
