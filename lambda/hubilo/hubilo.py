import datetime
import json
import logging
import os
from pprint import pformat
import string
import secrets
from urllib import parse
import urllib3

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

import eloqua

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')

HUBILO_TOKEN = os.environ['HUBILO_TOKEN']
QUEUE_URL = os.environ['QUEUE_URL']
TABLE_NAME = os.environ['TABLE_NAME']

table = dynamodb.Table(TABLE_NAME)

KEY = os.environ['SMTP_KEY']
SECRET = os.environ['SMTP_SECRET']

http_auth = KEY + ':' + SECRET
headers = urllib3.make_headers(basic_auth=http_auth)

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
        config['hubilo_event_id'] =  item['HubiloId']
        config['eloqua_parent_id'] =  item['EloquaCDOParentId']
        logger.debug("config: " + str(config))
        
    except Exception as e:
        logger.error(str(e))
        logger.error(event_id + ' is not defined.')

    return config

def executeRegistration(data, config):
    logger.debug("execute registration")

    HUBILO_ENDPOINT = f"https://{config['hostname']}/api/v1/integration/user/create"
    
    logger.debug(f"HUBILO_ENDPOINT: {HUBILO_ENDPOINT}")
    
    params = f"firstname={data['given_name']}"
    params += f"&lastname={data['family_name']}"
    params += f"&email={data['email']}"
    params += f"&organisation={data['company']}"
    params += f"&designation={data['job_title']}"
    params += f"&country={data['country']}"
    params += f"&eventid={config['hubilo_event_id']}"
    
    
    logger.debug(f"params: " + pformat(params))

    token = f"Bearer {HUBILO_TOKEN}"
    
    logger.debug(f"token: " + pformat(token))
    
    headers = {
        "Authorization" : token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    logger.debug(f"headers: " + pformat(headers))

    r = http.request_encode_body("POST", HUBILO_ENDPOINT, body=params, headers=headers)
    
    res = json.loads(r.data)
    logger.debug(f"Hubilo Enrollment [status: {r.status}, res: " + pformat(res) + "]")

    if res['status'] == 200:
        return True
    else:
        return False

def lambda_handler(event, context):
    logger.debug("hubilo")
    logger.debug("Event: " + str(event))
    
    eloqua_controller = eloqua.eloqua_controller(headers)

    try:
        for record in event['Records']:
            body = record['body']

            logger.debug("Body: " + str(body))

            data = json.loads(body)
        
            event_id = data['event_id']

            config = get_config(event_id)
            logger.debug("config: " + str(config))
            
            if executeRegistration(data, config):
                logger.debug(f"Registration successful")
                status = eloqua_controller.createCustomDataObject(config['eloqua_parent_id'],data['email'])
                if status != 200 and status !=201:
                    logger.error("Error creating custom data object")
            else:
                logger.error(f"Error registering user {data['email']}")

            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=record['receiptHandle']
            )
    except Exception as e:
        logger.error("Error processing registration: " + str(e))
        exit()