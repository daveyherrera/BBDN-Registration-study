
import base64
import json
import logging
import os

from urllib import parse as urlparse

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Looking for environment variable called "IP_WHITELIST" and splits them using | as the separator
IP_WHITELIST = os.environ['IP_WHITELIST'].split("|")

# defines the level of logging based on environment variable.
LOG_LEVEL = os.environ['LOG_LEVEL']
# defines the logger in a variable as an instance to set its level.
logger = logging.getLogger()

# depending on the value within the environment variable, the level of logging is defined.
if LOG_LEVEL == "DEBUG":
    logger.setLevel(logging.DEBUG)
elif LOG_LEVEL == "ERROR":
    logger.setLevel(logging.ERROR)
elif LOG_LEVEL == "WARN":
    logger.setLevel(logging.WARN)
else:
    logger.setLevel(logging.INFO)

# Function created to validate if the remote ip is within the valid ips
def limit_remote_addr(remote_ip, allowed_ips):

# writes the remote ip within the debug logger
    logger.debug(str(remote_ip))
# sets the ip match as false by default
    ip_match = False
# lop that compares if the ip addres is within the allowed IPs
    for ip_address in allowed_ips:
        # writes into the debug log the text "Allowed IP" Followed by the ip within the loop
        logger.debug("Allowed IP: " + str(ip_address))
        # If the remote ip is within the list of white listed ips, once a match is found it sets ip_match to true and breaks out
        if remote_ip == ip_address:
            ip_match = True
            break
    # otherwise if ip_match reminds false it logs an error with invalid Ip Address3
    if ip_match == False:        
        logger.error("Invalid IP address: " + str(remote_ip))
    # it returns the ip_match value (true or false)
    return(ip_match)

# Defines a handler for lambda passing event and context
def lambda_handler(event, context):
    # writes "authorizer" in the debug log
    logger.debug("authorizer")
    # writes "event" and the event itself
    logger.debug("Event: " + str(event))
    # creates the source_ip var and event gets headers and x-forwared-for attributes
    source_ip = event['headers']['x-forwarded-for']
    # writes the source ip into the debug log
    logger.debug("source_ip: " + str(source_ip))
    # if the lenght of the iP_WHITELIST is bigger than zero and the first one in the array is not empty
    if len(IP_WHITELIST) > 0 and IP_WHITELIST[0] != "":
        # if when evaluating the function it returns false
        if limit_remote_addr(source_ip, IP_WHITELIST) == False:
            # returns a dict (json) with false autorization
            return { "isAuthorized": False }
    # else it writes a logger line saying it passed with a list of whitelisted ips
    logger.debug("Passed: " + str(IP_WHITELIST))
    # returns true and a (json) dictionary with True
    return  { "isAuthorized": True }
