#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from parse_response import parse_response
BASE_URL = 'https://pythoncanarias.es'


def get_tracks_information() -> object:
    url = 'https://pythoncanarias.es/api/v1/events/pydaygc19/tracks'
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


def create_tracks_cards(tracks_information: list, selected_track: int = None):
    if selected_track == 1:
        track_one_information = tracks_information['result'][0]['schedule']
        track_one = []
        for track_info in track_one_information:
            track_one.append(create_card(track_info))
        track_cards = track_one
    elif selected_track == 2:
        track_two_information = tracks_information['result'][1]['schedule']
        track_two = []
        for track_info in track_two_information:
            track_two.append(create_card(track_info))
        track_cards = track_two
    else:
        tracks = []
        track_one_information = tracks_information['result'][0]['schedule']
        track_two_information = tracks_information['result'][1]['schedule']
        tracks.append(
            {
                "text": {
                    "text": [
                        "En el Track 1 {} se impartirán las siguientes ponencias".format(
                            tracks_information['result'][0]['name']
                        )
                    ]
                },
                "platform": "TELEGRAM"
            },
        )
        for track_info in track_one_information:
            tracks.append(create_card(track_info))
        tracks.append(
            {
                "text": {
                    "text": [
                        "En el Track 2 {} se impartirán las siguientes ponencias".format(
                            tracks_information['result'][1]['name']
                        )
                    ]
                },
                "platform": "TELEGRAM"
            },
        )
        for track_info in track_two_information:
            tracks.append(create_card(track_info))
        track_cards = tracks
    return track_cards


def tracks_action(req: object = None) -> object:
    """tracks action
    """
    tracks_information = get_tracks_information()
    if req['queryResult']['parameters']['number']:
        selected_track = int(req['queryResult']['parameters']['number'])
        tracks_cards = create_tracks_cards(tracks_information, selected_track)
    else:
        tracks_cards = create_tracks_cards(tracks_information)
    result = {"fulfillmentMessages": []}
    for track_card in tracks_cards:
        result['fulfillmentMessages'].append(track_card)
    response = parse_response(result)
    return response
