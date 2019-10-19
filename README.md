# Canpy 2019. Bot Telegram PyDayGC19

Bot para Telegram del evento del PyDayGC19 celebrado en las Palmas de Gran Canaria

Este agente está principalmente enfocado a ser utilizado con Google Assistant ya que utiliza en las respuestas el lenguaje SSML de asistentes de voz

## Tecnologías utilizadas

* Dialogflow
* Flask
* Python

## Intenciones creadas

Cada una de las intenciones tiene una función y un conjunto de frases de entrenamiento

# IMPORTANTE

Para utilizarlo en modo desarrollo, es necesario utilizar la herramienta [Ngrok](https://ngrok.com/) porque Dialogflow al asignar la opción de fulfillment necesita una dirección https y Ngrok te permite hacer un túnel a través de tu localhost y generar una dirección https.

## Instalar dependencias

Para instalar las dependencias crear un entorno virtual

```shell
virtualenv env
```

Activarlo `source env/bin/activate` en unix ó  `env/Script/activate` en windows. Posteriormente, instalar los paquetes mediante `pip install -r requirement.txt`