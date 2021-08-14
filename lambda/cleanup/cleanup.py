import datetime
import json
import logging
import os
import string
import secrets
import urllib3

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

import auth_provider, rest_controller

TOKEN_LIST = {}

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['TABLE_NAME']

table = dynamodb.Table(TABLE_NAME)

http = urllib3.PoolManager()

LOG_LEVEL = os.environ['LOG_LEVEL']
logger = logging.getLogger()

if LOG_LEVEL == "DEBUG":
    logger.setLevel(logging.DEBUG)
elif LOG_LEVEL == "ERROR":
    logger.setLevel(logging.ERROR)
elif LOG_LEVEL == "WARN":
    logger.setLevel(logging.WARN)
else:
    logger.setLevel(logging.INFO)

def get_config(event_id):

    results = table.query(KeyConditionExpression=Key("Event").eq(event_id))
    
    config = {}
    
    try:
        item = results['Items'][0]
        logger.debug("item: " + str(item))
        
        config['hostname'] = item['HostName']
        config['datasource'] =  item['Datasource']

        logger.debug("config: " + str(config))
        
    except Exception as e:
        logger.error(str(e))
        logger.error(event_id + ' is not defined.')

    return config

def deleteExpiredUsers(event_id, config):
    
    global TOKEN_LIST
    logger.debug("delete expired users")

    auth = auth_provider.auth_provider(config['hostname'])
    
    VALID_TOKEN = True
    token = ""
    
    if not bool(TOKEN_LIST):
        logger.debug("TOKEN_LIST is empty")
        VALID_TOKEN = False
    else:
        try: 
            token = TOKEN_LIST[event_id]
            if auth.test_token(token) == False:
                VALID_TOKEN = False
        except:
            VALID_TOKEN = False
        
    logger.debug("Valid Token = " + str(VALID_TOKEN))
    
    
    if VALID_TOKEN == False:         
        token = auth.requestBasicToken()

        if token is None:
            exit()

        TOKEN_LIST[event_id] = token
        
    logger.debug ("Token is " + token)

    rest = rest_controller.rest_controller(token,config['hostname'])

    rest.deleteExpiredUsers(rest.getDataSourceId(config['datasource']))

def lambda_handler(event, context):
    logger.debug("process")
    logger.debug("Event: " + str(event))

    try:
        deleteExpiredUsers("blackboard-trial", get_config("blackboard-trial"))

    except Exception as e:
        logger.error("Error processing cleanup: " + str(e))
        exit()
    
    return 200