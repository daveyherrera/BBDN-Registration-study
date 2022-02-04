import base64
import datetime
import json
import logging
import os
import string
import secrets
import urllib3

from urllib import parse as urlparse

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

import auth_provider, rest_controller, snowflake_controller

#SNOWFLAKE_QUEUE_URL = os.environ['SNOWFLAKE_QUEUE_URL']

TOKEN = None

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
    

def get_body(event):
    return base64.b64decode(str(event['body'])).decode('ascii')
    

def validate_post(event):
    if "origin" in event['headers']:
        return event["headers"]["origin"] == "https://bde.bbdevcon.com"
    else:
        return False
        
def get_config():

    results = table.query(KeyConditionExpression=Key("Event").eq('data-explorers'))
    
    config = {}
    
    try:
        item = results['Items'][0]
        logger.debug("item: " + str(item))
        
        config['hostname'] = item['HostName']
        config['course_ids'] =  item['CourseIds'].split("|")
        config['datasource'] =  item['Datasource']
        logger.debug("config: " + str(config))
        
    except Exception as e:
        logger.error(str(e))
        logger.error('data_explorers event is not defined.')

    return config

def generate_password():
        
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    
    return password


def getToken(config):
    global TOKEN
    logger.debug("execute registration")

    auth = auth_provider.auth_provider(config['hostname'])
    
    VALID_TOKEN = True
    token = ""
    
    if TOKEN is None:
        logger.debug("TOKEN is empty")
        VALID_TOKEN = False
    else:
        try: 
            token = TOKEN
            if auth.test_token(token) == False:
                VALID_TOKEN = False
        except:
            VALID_TOKEN = False
        
    logger.debug("Valid Token = " + str(VALID_TOKEN))
    
    
    if VALID_TOKEN == False:         
        token = auth.requestBasicToken()

        if token is None:
            exit()

        TOKEN = token
        
    logger.debug ("Token is " + token)
    
    return token
    

def create_user(rest,email,password,datasource,given_name,family_name,job_title,company):
    
    role = 'Student'
    
    user_json = {
        "userName": email,
        "password": password,
        "dataSourceId":datasource,
        "availability": {
            "available": "Yes"
        },
        "name": {
            "given": given_name,
            "family": family_name
        },
        "job": {
            "title": job_title,
            "company": company
        },
        "contact": {
            "email": email
        },
        "institutionRoleIds" : [ role ]
    }
    
    student = rest.createLearnUser(user_json)
    
    return student


def enrollUserInCourse(rest,config,email):
    role = 'Student'
    
    courseId = ""
    for course_data in config['course_ids']:
        course_info = course_data.split("^")
        course_id = course_info[0]
        
    
    enrollment = rest.enrollUserInCourse(course_id, email, role)
    logger.debug(f"Enrollment: {enrollment}")
    
    return enrollment


def lambda_handler(event, context):
    logger.debug("api")
    logger.debug(f"Event: {event}")
    logger.debug(f"Context: {context}")
    
    login_info = {}
    
    try:
        #validate api call
        if validate_post(event) == False:
            return {
                'statusCode' : 401,
                'body' : 'You are unauthorized to access this endpoint',
                "headers": {
                    "Content-Type": "plain/text"
                }
            }
        
        #get post form data
        msg_map = dict(urlparse.parse_qsl(get_body(event)))  # data comes b64 and also urlencoded name=value& pairs
        logger.debug(str(msg_map))

        given_name = msg_map.get('fname','err')
        family_name = msg_map.get('lname','err')
        email = msg_map.get('email','err')
        company = msg_map.get('institution','err')
        job_title = msg_map.get('title','err')
        
        email = email.lower()
        
        #Get config from dynamo
        config = get_config()
        
        login_info['username'] = email
        
        #Get token
        token = getToken(config)
        
        #Generate password
        password = generate_password();
        
        #instantiate controllers
        rest = rest_controller.rest_controller(token,config['hostname'],config['datasource'])
        snowflake = snowflake_controller.snowflake_controller()
        
        #Create user if they do not exist
        if not rest.userExists(email):
            learn_password = password
            user = create_user(rest,email,password,config['datasource'],given_name,family_name,job_title,company)
            logger.debug(f"user created: {user}")
        else:
            learn_password = "UserExists"
            
        #Enroll user in course
        enrollment = enrollUserInCourse(rest,config,email)

        snowflake_username = snowflake.generate_username_from_email(email)

        snowflake_info = {
            'username': snowflake_username,
            'password': password,
            'first': given_name,
            'last': family_name,
            'email': email
        }

        snowflake.create_snowflake_user(snowflake_info)
        
        return {
            'statusCode' : 302,
            "headers": {
                "Content-Type": "application/json",
                "Location": f"https://bde.bbdevcon.com/confirmation.html?username={email}&learn_password={learn_password}&sf_user={snowflake_username}&sf_pass={password}"
            }
        }
        
        
    except Exception as e:
        logger.error("Error processing registration: " + str(e))
        exit()