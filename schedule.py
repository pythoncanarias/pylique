#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from parse_response import parse_response
BASE_URL = 'https://pythoncanarias.es'


def get_schedule_information() -> object:
    url = 'https://pythoncanarias.es/api/v1/events/pydaygc19/talks'
    response = requests.get(url)
    data = response.json()
    return data


def create_speaker_cards(schedule_information: list) -> list:
    speakers = []
    for speaker in schedule_information['result']:
        speakers.append(
            {
                "card": {
                    "title": "{} {}.\n{}.\n\nComienzo:{}\n\nFin:{}\n\n".format(
                        speaker['speakers'][0]['name'],
                        speaker['speakers'][0]['surname'],
                        speaker['name'],
                        speaker['start'],
                        speaker['end']),
                    "subtitle": speaker['description'],
                    "imageUri": BASE_URL + speaker['speakers'][0]['photo'],
                    "buttons": [
                        {
                            "text": "prueba button"
                        }
                    ]
                },
                'platform': 'TELEGRAM',
            }
        )
    return speakers


def schedule_action(req: object = None) -> object:
    """schedule action
    """
    schedule_information = get_schedule_information()
    speaker_cards = create_speaker_cards(schedule_information)
    result = {"fulfillmentMessages": []}
    for speaker_card in speaker_cards:
        result['fulfillmentMessages'].append(speaker_card)
    response = parse_response(result) 
    return response
