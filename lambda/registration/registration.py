import base64
import json
import logging
import os

from urllib import parse as urlparse

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')

QUEUE_URL = os.environ['QUEUE_URL']
HUBILO_QUEUE_URL = os.environ['HUBILO_QUEUE_URL']
TABLE_NAME = os.environ['TABLE_NAME']

table = dynamodb.Table(TABLE_NAME)

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

is_hubilo = False

def get_body(event):
    return base64.b64decode(str(event['body'])).decode('ascii')
    
def is_valid_event(event_id):
    global is_hubilo

    results = table.query(KeyConditionExpression=Key("Event").eq(event_id))

    try:
        item = results['Items'][0]
        is_hubilo = item['IsHubilo']
        logger.debug(f"config['is_hubilo']: {is_hubilo}]")
        return True
    except:
        logger.error(event_id + ' is not defined.')
        return False

    return 

def lambda_handler(event, context):
    global is_hubilo
    
    logger.debug("register")
    logger.debug("Event: " + str(event))

    try:
        msg_map = dict(urlparse.parse_qsl(get_body(event)))  # data comes b64 and also urlencoded name=value& pairs
        logger.debug(str(msg_map))

        given_name = msg_map.get('firstName','err')
        family_name = msg_map.get('lastName','err')
        email = msg_map.get('emailAddress','err')
        company = msg_map.get('company','err')
        job_title = msg_map.get('title','err')
        phone = msg_map.get('busPhone','err')
        country = msg_map.get('country','err')
        industry = msg_map.get('industry','err')
        event_id = msg_map.get('hiddenField','err')
        
        if not is_valid_event(event_id):
            retval={
                'statusCode' : 404,
                'body' : 'Invalid Event Id',
                "headers": {
                    "Content-Type": "text/plain"
                }
            }
            logger.error(str(retval))
            return retval
        
        message = {
            'username': email,
            'given_name': given_name,
            'family_name': family_name,
            'email': email,
            'company': company,
            'job_title': job_title,
            'country': country,
            'industry': industry,
            'event_id' : event_id
        }
        
        logger.debug(str(message))
        
        logger.debug(f"is hubilo = {is_hubilo} HUBILO_QUEUE_URL is {HUBILO_QUEUE_URL}")

        params = {
            'QueueUrl' : QUEUE_URL if is_hubilo == False else HUBILO_QUEUE_URL,
            'MessageBody' : message
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL if is_hubilo == False else HUBILO_QUEUE_URL,
            MessageBody=(
                json.dumps(message)
            )
        )
        
        return {
            'statusCode' : 202,
            'body' : json.dumps(message),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        logger.error("Error processing registration: " + str(e))
        return {
            'statusCode' : 500,
            'body' : "Error processing registration: " + str(e)
        }