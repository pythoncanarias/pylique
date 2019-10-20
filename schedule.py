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


def create_card(speaker_info: object) -> object:
    return {
                "card": {
                    "title": "{} {}.\n{}.\n\nComienzo:{}\n\nFin:{}\n\n".format(
                        speaker_info['speakers'][0]['name'],
                        speaker_info['speakers'][0]['surname'],
                        speaker_info['name'],
                        speaker_info['start'],
                        speaker_info['end']),
                    "subtitle": speaker_info['description'],
                    "imageUri": BASE_URL + speaker_info['speakers'][0]['photo'],
                    "buttons": [
                        {
                            "text": "prueba button"
                        }
                    ]
                },
                'platform': 'TELEGRAM',
            }
def create_speaker_cards(schedule_information: list, speaker_schedule: list = []) -> list:
    speakers = []
    if len(speaker_schedule) == 0:
        for speaker in schedule_information['result']:
            speakers.append(create_card(speaker))
    else:
        for speaker in schedule_information['result']:
            splited_name = speaker['speakers'][0]['name'].split()
            splited_surname = speaker['speakers'][0]['surname'].split()
            if speaker_schedule[0] in splited_name or \
               speaker_schedule[0] in splited_surname or \
               speaker['speakers'][0]['name'] + speaker['speakers'][0]['surname'] == speaker_schedule[0]:
                speakers.append(create_card(speaker))
    return speakers


def schedule_action(req: object = None) -> object:
    """schedule action
    """
    schedule_information = get_schedule_information()
    if req['queryResult']['parameters']['speaker_entities']:
        speaker_schedule = req['queryResult']['parameters']['speaker_entities']
        speaker_cards = create_speaker_cards(schedule_information, speaker_schedule)
    else:
        speaker_cards = create_speaker_cards(schedule_information)
    result = {"fulfillmentMessages": []}
    for speaker_card in speaker_cards:
        result['fulfillmentMessages'].append(speaker_card)
    response = parse_response(result) 
    return response
