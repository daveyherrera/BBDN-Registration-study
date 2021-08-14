
import base64
import json
import logging
import os

from urllib import parse as urlparse

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

IP_WHITELIST = os.environ['IP_WHITELIST'].split("|")

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

def limit_remote_addr(remote_ip, allowed_ips):

    logger.debug(str(remote_ip))
    
    ip_match = False
    
    for ip_address in allowed_ips:
        logger.debug("Allowed IP: " + str(ip_address))
        if remote_ip == ip_address:
            ip_match = True
            break
    
    if ip_match == False:        
        logger.error("Invalid IP address: " + str(remote_ip))
    
    return(ip_match)

def lambda_handler(event, context):
    logger.debug("authorizer")
    logger.debug("Event: " + str(event))

    source_ip = event['headers']['x-forwarded-for']

    logger.debug("source_ip: " + str(source_ip))

    if len(IP_WHITELIST) > 0 and IP_WHITELIST[0] != "":
        if limit_remote_addr(source_ip, IP_WHITELIST) == False:
            return { "isAuthorized": False }
    
    logger.debug("Passed: " + str(IP_WHITELIST))
    
    return  { "isAuthorized": True }
    