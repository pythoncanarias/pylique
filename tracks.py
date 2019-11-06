#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
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
                    "text": f"{speaker_info['speakers'][0]['name']} {speaker_info['speakers'][0]['surname']}"
                }
            ]
        },
        'platform': 'TELEGRAM',
    }


def create_tracks_cards(tracks_information: list, selected_track: int = None, speaker_specific_hour: str = None) -> object:
    if selected_track == 1:
        track_one_information = tracks_information['result'][0]['schedule']
        track_one = []
        for track_info in track_one_information:
            print(track_info)
            if speaker_specific_hour:
                if datetime.datetime.strptime(speaker_specific_hour,'%H:%M') >=  datetime.datetime.strptime(track_info['start'],'%H:%M') and datetime.datetime.strptime(speaker_specific_hour, '%H:%M') <=  datetime.datetime.strptime(track_info['end'], '%H:%M'):
                    track_one.append(create_card(track_info))
                    break
            else:
                track_one.append(create_card(track_info))
        track_cards = track_one
    elif selected_track == 2:
        track_two_information = tracks_information['result'][1]['schedule']
        track_two = []
        for track_info in track_two_information:
            if speaker_specific_hour:
                if datetime.datetime.strptime(speaker_specific_hour,'%H:%M') >=  datetime.datetime.strptime(track_info['start'],'%H:%M') and datetime.datetime.strptime(speaker_specific_hour, '%H:%M') <=  datetime.datetime.strptime(track_info['end'], '%H:%M'):
                    track_one.append(create_card(track_info))
                    break
            else:
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

def get_speaker_specific_hour():
    return ''.join(str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute))


def get_next_speaker():
    return ''.join(str(datetime.datetime.now().hour + 1 ) + ':' + str(datetime.datetime.now().minute))


def tracks_action(req: object = None) -> object:
    """tracks action
    """
    tracks_information = get_tracks_information()
    if req['queryResult']['parameters']['number']:
        selected_track = int(req['queryResult']['parameters']['number'])
        if req['queryResult']['parameters']['now_entities']:
            speaker_specific_hour = get_speaker_specific_hour()
            tracks_cards = create_tracks_cards(tracks_information, selected_track, speaker_specific_hour)
        else:
            tracks_cards = create_tracks_cards(tracks_information, selected_track)
        if req['queryResult']['parameters']['next_entities']:
                speaker_specific_hour = get_next_speaker()
                tracks_cards = create_tracks_cards(tracks_information, selected_track, speaker_specific_hour)
    else:
        if req['queryResult']['parameters']['now_entities']:
            speaker_specific_hour = get_speaker_specific_hour()
            if req['queryResult']['parameters']['next_entities']:
                speaker_specific_hour = get_next_speaker()
            tracks_cards = create_tracks_cards(tracks_information, speaker_specific_hour)
        else:
            tracks_cards = create_tracks_cards(tracks_information)
        if req['queryResult']['parameters']['next_entities']:
                speaker_specific_hour = get_next_speaker()
                tracks_cards = create_tracks_cards(tracks_information, selected_track, speaker_specific_hour)
    result = {"fulfillmentMessages": []}
    for track_card in tracks_cards:
        result['fulfillmentMessages'].append(track_card)
    response = parse_response(result)
    return response
