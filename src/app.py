# -*- coding: utf-8 -*-

import boto3
import os
import logging
import hashlib
import json
from PIL import Image
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from pprint import pprint
import dialogflow
from google.api_core.exceptions import InvalidArgument
#import wget, urllib, os
import requests
# https://pypi.org/project/extcolors/           pip install extcolors
import extcolors
# https://webcolors.readthedocs.io/en/1.11.1/   pip install webcolors
import webcolors
from selectorlib import Extractor

import src.imagereko
import src.scrap



def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    try:
        print("Evento recebido : "+str(event))
        resposta = hello(event)
    #    ip = requests.get("http://checkip.amazonaws.com/")
    
    except Exception as e:
    #     # Send some context about this error to Lambda Logs
        print(e)
        raise e

    return {
        "statusCode": 200,
        "body": resposta, #json.dumps({
            #"message": resposta,
            # "location": ip.text.replace("\n", "")
        #}),
    }

region_name='us-east-1'
bucket='megahack'
s3_client = boto3.client('s3')

# https://www.twilio.com/blog/building-backup-whatsapp-chatbot-python-flask-twilio
#@app.route('/webhook', methods=['POST'])
def hello(events):
        # Replace no codigo : req.values -> events
        #pprint(str(req.values))
        pprint(events)
        num_media = int(events['NumMedia'])
        phone_number = events['From']
        resp = MessagingResponse()

        if num_media > 0:
            try:
                enviar_statuszap("Imagem recebida.", phone_number)
                return imagem(request)
            except Exception as e:
                resp.message("Infelizmente tive uma erro durante a analise da Imagem enviada.")
                print('\tErro ao processar imagem')
                logging.error(e)
                return str(resp)
        else:
            pergunta = events['Body']
            if pergunta.startswith('http'):     #SCRAP EXTRACTOR
                enviar_statuszap("Link para analise (scrap) recebido.", phone_number)
                try: 
                    resposta = str(scrape(pergunta, phone_number))
                    #resp.message(resposta)
                    resp.message('Os campos analisados podem utilizados por você automaticamente para ganhar agilidade.')
                    return str(resp)
                except Exception as e:
                    resp.message("Infelizmente tive um erro ao tentar analisar a página.")
                    print('\tErro no scrap')
                    logging.error(e)
                    return str(resp)
            else:                               #DIALOGFLOW
                #enviar_statuszap("Duvida recebida.", phone_number)
                try:
                    resposta = dialog(pergunta)
                    resp.message(resposta)
                    return str(resp)
                except Exception as e:
                    resp.message("Infelizmente tive uma erro ao integrar com o motor do ChatBot")
                    print('\tErro ao falar com o Dialogflow')
                    logging.error(e)
                    return str(resp)

def enviar_statuszap(texto, user_phone_number):
    return client.messages.create(
            from_='whatsapp:+14155238886',
            body=texto,
            to=user_phone_number
        )
