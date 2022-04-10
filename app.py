from re import A
from flask import  Flask, jsonify, request
from flask_restful import Resource,Api

from dataclasses import replace
import spacy
import tweepy
from tweepy import OAuthHandler
import replaceall
from replaceall import replaceall
from flask_mysqldb import MySQL
from datetime import datetime
from pycorenlp import StanfordCoreNLP
import json

nlp = spacy.load("./output/model-last")

consumer_key = "Jv0DKLySkVhApn5wqWncwYdXA"
consumer_secret = "6l9mcrFK2LOqwtYLPv44f8lRouNErwRMf0amY1F9139qcoXyQB"
access_token = "1327697310852263936-iY1jE227HA8PReLGtdMjD5v2yj6IME"
access_token_secret = "zsl6wQjuOItu3MlUGpjjmQZVzYCJsUzynzWSEhMBpJS3P"

palabraClave = "veneco"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
apii = tweepy.API(auth)

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_tesis'

nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
mysql = MySQL(app)

contNeu = 0
contNeg = 0 
contPos = 0

palabrasvac = ['él', 'ésta', 'éstas', 'éste', 'éstos', 'el']
palabrasvac += ['última', 'últimas', 'último', 'últimos']
palabrasvac += ['a', 'añadió', 'aún', 'actualmente', 'adelante']
palabrasvac += ['además', 'afirmó', 'agregó', 'ahí', 'ahora', 'al']
palabrasvac += ['algún', 'algo', 'alguna', 'algunas', 'alguno', 'algunos']
palabrasvac += ['alrededor', 'ambos', 'ante', 'anterior', 'antes',]
palabrasvac += ['apenas', 'aproximadamente', 'aquí', 'así']
palabrasvac += ['aseguró', 'aunque', 'ayer', 'bajo', 'bien', 'buen']
palabrasvac += ['buena', 'buenas', 'bueno', 'buenos', 'cómo', 'cada']
palabrasvac += ['casi', 'cerca', 'cierto', 'cinco', 'comentó', 'como']
palabrasvac += ['con', 'conocer', 'consideró', 'considera', 'contra']
palabrasvac += ['cosas', 'creo', 'cual', 'cuales', 'cualquier', 'cuando']
palabrasvac += ['cuanto', 'cuatro', 'cuenta', 'da', 'dado', 'dan', 'dar']
palabrasvac += ['de', 'debe', 'deben', 'debido', 'decir', 'dejó', 'del']
palabrasvac += ['demás', 'dentro', 'desde', 'después', 'dice', 'dicen']
palabrasvac += ['dicho', 'dieron', 'diferente', 'diferentes', 'dijeron']
palabrasvac += ['dijo', 'dio', 'donde', 'dos', 'durante', 'e', 'ejemplo']
palabrasvac += ['el', 'ella', 'ellas', 'ello', 'ellos', 'embargo', 'en']
palabrasvac += ['encuentra', 'entonces', 'entre', 'era', 'eran', 'es']
palabrasvac += ['esa', 'esas', 'ese', 'eso', 'esos', 'está', 'están', 'esta']
palabrasvac += ['estaba', 'estaban', 'estamos', 'estar', 'estará', 'estas']
palabrasvac += ['este', 'esto', 'estos', 'estoy', 'estuvo', 'ex', 'existe']
palabrasvac += ['existen', 'explicó', 'expresó', 'fin', 'fue', 'fuera']
palabrasvac += ['fueron', 'gran', 'grandes', 'ha', 'había', 'habían']
palabrasvac += ['haber', 'habrá', 'hace', 'hacen', 'hacer', 'hacerlo']
palabrasvac += ['hacia', 'haciendo', 'han', 'hasta', 'hay', 'haya']
palabrasvac += ['he', 'hecho', 'hemos', 'hicieron', 'hizo', 'hoy']
palabrasvac += ['hubo', 'igual', 'incluso', 'indicó', 'informó']
palabrasvac += ['junto', 'la', 'lado', 'las', 'le', 'les', 'llegó']
palabrasvac += ['lleva', 'llevar', 'lo', 'los', 'luego', 'lugar']
palabrasvac += ['más', 'manera', 'manifestó', 'mayor', 'me', 'mediante']
palabrasvac += ['mejor', 'mencionó', 'menos', 'mi', 'mientras', 'misma']
palabrasvac += ['mismas', 'mismo', 'mismos', 'momento', 'mucha', 'muchas']
palabrasvac += ['mucho', 'muchos', 'muy', 'nada', 'nadie', 'ni', 'ningún']
palabrasvac += ['ninguna', 'ningunas', 'ninguno', 'ningunos', 'no', 'nos']
palabrasvac += ['nosotras', 'nosotros', 'nuestra', 'nuestras', 'nuestro']
palabrasvac += ['nuestros', 'nueva', 'nuevas', 'nuevo', 'nuevos', 'nunca']
palabrasvac += ['o', 'ocho', 'otra', 'otras', 'otro', 'otros', 'para']
palabrasvac += ['parece', 'parte', 'partir', 'pasada', 'pasado', 'pero']
palabrasvac += ['pesar', 'poca', 'pocas', 'poco', 'pocos', 'podemos']
palabrasvac += ['podrá', 'podrán', 'podría', 'podrían', 'poner', 'por']
palabrasvac += ['porque', 'posible', 'próximo', 'próximos', 'primer']
palabrasvac += ['primera', 'primero', 'primeros', 'principalmente', 'propia']
palabrasvac += ['propias', 'propio', 'propios', 'pudo', 'pueda']
palabrasvac += ['puede', 'pueden', 'pues', 'qué', 'que', 'quedó']
palabrasvac += ['queremos', 'quién', 'quien', 'quienes', 'quiere']
palabrasvac += ['realizó', 'realizado', 'realizar', 'respecto', 'sí']
palabrasvac += ['sólo', 'se', 'señaló', 'sea', 'sean', 'según', 'segunda']
palabrasvac += ['segundo', 'seis', 'ser', 'será', 'serán', 'sería', 'si']
palabrasvac += ['sido', 'siempre', 'siendo', 'siete', 'sigue', 'siguiente']
palabrasvac += ['sin', 'sino', 'sobre', 'sola', 'solamente', 'solas', 'solo']
palabrasvac += ['solos', 'son', 'su', 'sus', 'tal', 'también', 'tampoco']
palabrasvac += ['tan', 'tanto', 'tenía', 'tendrá', 'tendrán', 'tenemos']
palabrasvac += ['tener', 'tenga', 'tengo', 'tenido', 'tercera', 'tiene']
palabrasvac += ['tienen', 'toda', 'todas', 'todavía', 'todo', 'todos']
palabrasvac += ['total', 'tras', 'trata', 'través', 'tres', 'tuvo']
palabrasvac += ['un', 'una', 'unas', 'uno', 'unos', 'usted', 'va']
palabrasvac += ['vamos', 'van', 'varias', 'varios', 'veces', 'ver']
palabrasvac += ['vez', 'y', 'ya', 'yo']


class Helloworld(Resource):
    def get(self,numero):
        diccionario = {}
        i = 1
        for tweet in tweepy.Cursor(apii.search_tweets, palabraClave, tweet_mode='extended' ,country= "Colombia").items(numero):
            twet =  replaceall(tweet._json['full_text'],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]")
            twet = twet.replace("RT","")
            doc = nlp(twet)
            if(len(doc.ents) >= 2):
                diccionario[i] = {
                    "id":tweet._json['id'], 
                    "nombre":tweet._json["user"]["name"],
                    "texto": tweet._json['full_text'], 
                    "xenofobico": "Es xenofobico",
                    "imagen":tweet._json["user"]["profile_image_url"],
                    "localicacion":tweet._json["user"]["location"],
                    "Pais":tweet._json["place"],
                }
            else:
                diccionario[i] = {
                    "id":tweet._json['id'],
                    "nombre":tweet._json["user"]["name"],
                    "texto": tweet._json['full_text'], 
                    "xenofobico": "No Es xenofobico",
                    "imagen":tweet._json["user"]["profile_image_url"],
                    "localicacion":tweet._json["user"]["location"],
                    "Pais":tweet._json["place"],
                }
            i = i + 1
        response = jsonify(diccionario)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
api.add_resource(Helloworld, "/data/<int:numero>", endpoint="numero")

class Filter(Resource):
    def get(self, fechaI, fechaF, ubicacion):
        datos = ()
        diccionario = {}
        cur = mysql.connection.cursor()
        j = 0
        geolocalizacion = ""
        if ubicacion == "Cali":
            geolocalizacion = "3.429242,-76.522159,17km"
        elif ubicacion == "Bogota":
            geolocalizacion = "4.649491,-74.109285,18km"
        elif ubicacion == "Medellin":
            geolocalizacion = "6.250345,-75.579495,18km"
        elif ubicacion == "Barranquilla":
            geolocalizacion = "10.980820,-74.801851,10km"
        elif ubicacion == "Bucaramanga":
            geolocalizacion = "7.117082,-73.118824,8km"
        elif ubicacion == "Cucuta":
            geolocalizacion = "7.902638, -72.505451,6km"
        
        for tweet in apii.search_tweets(q=palabraClave, count=100, since=fechaI, until=fechaF, geocode=geolocalizacion):    
            fecha = tweet._json["created_at"].split(" ")[1]+"/"+tweet._json["created_at"].split(" ")[2]+"/"+tweet._json["created_at"].split(" ")[5]
            objDate = datetime.strptime(fecha, '%b/%d/%Y')
            date = datetime.strftime(objDate,'%Y-%m-%d')
            cur.execute(
                "INSERT IGNORE INTO histtwee(TWEEIDEN ,NOMBTWIT, FECHTWEE, UBICGEOG, TWEET, FOTOTWIT, RETWEET) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (  tweet._json['id'], 
                    tweet._json["user"]["name"],
                    date,
                    ubicacion,
                    tweet._json['text'], 
                    tweet._json["user"]["profile_image_url"],
                    tweet._json["retweet_count"],
                ))
            mysql.connection.commit()
        cur.close()

        with mysql.connection.cursor() as cursor:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT TWEEIDEN,NOMBTWIT,FECHTWEE,UBICGEOG,TWEET,FOTOTWIT,RETWEET FROM HistTwee WHERE FECHTWEE BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) AND UBICGEOG = %s", (fechaI,fechaF,ubicacion))
            datos = cursor.fetchall()

        for i in datos:
            twet =  replaceall(i[4],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]")
            twet = twet.replace("RT", "")
            doc = nlp(twet)
            if(len(doc.ents) >= 2):
                diccionario[j] ={
                    "id":i[0],
                    "nombre":i[1],
                    "fecha":str(i[2]),
                    "ubicacion":i[3],
                    "xenofobico": "Es xenofobico",
                    "texto":i[4],
                    "imagen": i[5],
                    "retweet": str(i[6]),
                }
            else:
                diccionario[j] ={
                    "id":i[0],
                    "nombre":i[1],
                    "fecha":str(i[2]),
                    "ubicacion":i[3],
                    "xenofobico": "No Es xenofobico",
                    "texto":i[4],
                    "imagen": i[5],
                    "retweet": str(i[6]),
                }
            j = j +1
        response = jsonify(diccionario)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
api.add_resource(Filter, "/filter/<fechaI>/<fechaF>/<ubicacion>", endpoint="fechaI fechaF ubicacion")

class db(Resource):
    def get(self, fechaI, fechaF, db):
        cur = mysql.connection.cursor()
        datos = ()
        diccionario = {
            "Cali" : 0,
            "Bogota": 0,
            "Medellin": 0,
            "Barranquilla":0,
            "Cucuta":0
        }
        with mysql.connection.cursor() as cursor:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT TWEEIDEN,NOMBTWIT,FECHTWEE,UBICGEOG,TWEET,FOTOTWIT,RETWEET FROM HistTwee WHERE FECHTWEE BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE)", (fechaI,fechaF))
            datos = cursor.fetchall()
        for i in datos:
            contNeg = 0
            twet =  replaceall(i[4],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]")
            twet = twet.replace("RT", "")
            doc = nlp(twet)
            
            if(db == "si"):
                if(len(doc.ents) >= 2):
                    diccionario[i[3]] += 1
            else :
                annot_doc = json.loads(nlp_wrapper.annotate(twet,properties={'annotators': 'sentiment', 'outputFormat': 'json', 'timeout': 100000,}))
                for sentence in annot_doc["sentences"]:
                    if (sentence["sentiment"] == 'Negative' or sentence["sentiment"] == 'Negativo') :
                        contNeg = contNeg+1
                        diccionario[i[3]] += contNeg   
            

        response = jsonify(diccionario)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
api.add_resource(db, "/db/<fechaI>/<fechaF>/<db>", endpoint="fechaI fechaF db")

class frecuencia(Resource):
    def get(self,fechaI, fechaF, ubi):
        datos = ()
        diccionario = {
            ubi : {},
        }
        with mysql.connection.cursor() as cursor:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT TWEEIDEN,NOMBTWIT,FECHTWEE,UBICGEOG,TWEET,FOTOTWIT,RETWEET FROM HistTwee WHERE FECHTWEE BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) AND UBICGEOG = %s", (fechaI,fechaF,ubi))
            datos = cursor.fetchall()
        for i in datos:
            texto = replaceall(i[4],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]")
            texto = texto.replace("RT", "")
            texto = texto.lower()
            
            #texto = quitarPalabrasvac(texto)
            texto = quitarPalabrasvac(texto)        
            palabras = texto.split(" ")
            

            for palabra in palabras:
                if palabra in diccionario[ubi]:
                    diccionario[ubi][palabra] += 1
                else:
                    diccionario[ubi][palabra] = 1
        lista = []
        for palabra in diccionario[ubi]:
            frecuencia = diccionario[ubi][palabra]
            lista.append({"word": palabra, "freq": frecuencia})

        diss = { ubi : lista }
        response = jsonify(diss)

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
api.add_resource(frecuencia, "/frecuencia/<fechaI>/<fechaF>/<ubi>", endpoint="fechaI fechaF ubi")

@app.route("/user/<userid>")
def get_user(userid):
    return userid


def quitarPalabrasvac(listaPalabras):
    palabra = ""
    for w in listaPalabras.split(" "):
        
        if w not in palabrasvac:
            palabra = palabra + " " + w
    return palabra
    #return [w for w in listaPalabras if w not in palabrasvac]