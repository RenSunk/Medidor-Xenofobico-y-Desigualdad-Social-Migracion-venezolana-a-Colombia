from dataclasses import replace
import spacy
import tweepy
from tweepy import OAuthHandler
import json
import replaceall
from replaceall import replaceall
import requests
import matplotlib.pyplot as plt
import pandas as pd

import emoji
from matplotlib import colors
import matplotlib.pyplot as barra
import matplotlib.pyplot as pie

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

nlp = spacy.load("./output/model-last")

date_since = "2021-10-28"
date_util = "2021-10-29"
nlp = spacy.load("es_core_news_sm")

consumer_key = "Jv0DKLySkVhApn5wqWncwYdXA"
consumer_secret = "6l9mcrFK2LOqwtYLPv44f8lRouNErwRMf0amY1F9139qcoXyQB"
access_token = "1327697310852263936-iY1jE227HA8PReLGtdMjD5v2yj6IME"
access_token_secret = "zsl6wQjuOItu3MlUGpjjmQZVzYCJsUzynzWSEhMBpJS3P"

palabraClave = "veneco"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

diccionario = {}
i = 1
for tweet in tweepy.Cursor(api.search_tweets, palabraClave).items(10):
    twet =  replaceall(tweet._json['text'],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]")
    twet = twet.replace("RT","")
    doc = nlp(twet)
        #print(twet)
        #print(doc.ents)
        #print(len(doc.ents))
    if(len(doc.ents) >= 2):
        diccionario[i] = { "texto": twet, "xenofobico": "Es xenofobico" }
    else:
        diccionario[i] = { "texto": twet, "xenofobico": "No Es xenofobico" }
    i = i + 1


def ia():
    print("aaa")
    return "hola"

    