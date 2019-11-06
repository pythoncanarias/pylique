#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parse_response import parse_response


def commands():
    return ''.join(
        '/track1 \n'
        '/track2 \n'
        '/agenda \n'
        '/ponencias \n'
        '/ponentes \n'
        '/ayuda \n'
        '/command \n'
        '/commands \n'
    )


def help_action(req: object = None) -> object:
    """help action
    """
    command_list = commands()
    result = {
        "fulfillmentMessages": [
            {
                "payload": {
                    "telegram": {
                        "text": f"""Estos son algunos de los comandos que puedes utilizar. \n\n {command_list}\n\n Además, puedes hablar con el bot sin necesidad de solo utilizar comandos. Ej: ponencias del pyday""",
                        "parse_mode": "Markdown"
                    }
                },
                "platform": "TELEGRAM",
            },
        ],
    }
    response = parse_response(result)
    return response
