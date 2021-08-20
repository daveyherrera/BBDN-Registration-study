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

sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']
EMAIL_QUEUE_URL = os.environ['EMAIL_QUEUE_URL']

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
        config['create_instructor'] =  item['CreateInstructor']
        config['instructor_role'] =  item['InstructorRole']
        config['create_student'] =  item['CreateStudent']
        config['student_role'] =  item['StudentRole']
        config['student_convention'] =  item['StudentConvention']
        config['course_ids'] =  item['CourseIds'].split("|")
        config['is_template'] =  item['IsTemplate']
        config['datasource'] =  item['Datasource']
        logger.debug("config: " + str(config))
        
    except Exception as e:
        logger.error(str(e))
        logger.error(event_id + ' is not defined.')

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

def create_user_json(data,instructor,password,role,datasource,student_convention=None):
    
    if len(role) == 0:
        if instructor:
            role = 'Faculty'
        else:
            role = 'Student'

    username = data['email']

    if not instructor:
        if student_convention[0] == '_':
            username = username + student_convention
        else:
            username = student_convention + username

    return({
        "userName": username,
        "password": password,
        "dataSourceId":datasource,
        "availability": {
            "available": "Yes"
        },
        "name": {
            "given": data['given_name'],
            "family": data['family_name']
        },
        "job": {
            "title": data['job_title'],
            "company": data['company']
        },
        "contact": {
            "email": data['email']
        },
        "address": {
            "country": data['country']
        },
        "institutionRoleIds" : [ role ]
    })

def executeRegistration(data, event_id, config):
    global TOKEN_LIST
    logger.debug("execute registration")

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

    login_info = {}

    rest = rest_controller.rest_controller(token,config['hostname'],config['datasource'])

    if rest.userExists(data):
        logger.error(f"User {data['email']} already exists in {config['hostname']}")
        login_info['user_exists'] = True
        return login_info

    password = generate_password()

    course_ids = config['course_ids']
    logger.debug("course_ids: " + str(course_ids))
    
    if config['is_template']:
        
        created_courses = []

        for course_data in course_ids:
            logger.debug("course_data: " + str(course_data))
            course_id = course_data.split("^")

            logger.debug("course_id: " + str(course_id))
            
            new_course_id = course_id[0].split('_')[1] + '_' + data['email'].replace('@', '_') + '_' + str(datetime.datetime.now().timestamp()).split(".")[0]
            logger.debug("new_course_id: " + new_course_id)
            created_courses.append(rest.createCourseFromTemplate(course_id[0], new_course_id, config['datasource']) + "^" + course_id[1] + "^" + course_id[2] + "^" + course_id[3])
        
        course_ids = created_courses

    if config['create_instructor']:
        
        instructor = rest.createLearnUser(create_user_json(data,True,password,config['instructor_role'],config['datasource']))

        login_info['instructor'] = instructor['userName']
        login_info['password'] = password
        login_info['created_date'] = instructor['created']
        
        logger.debug("CreateInstructor: course_ids: " + str(course_ids))
        
        for course_data in course_ids:
            course_id = course_data.split("^")
            logger.debug(f"CreateInstructor: course_id: {course_id}")
            course_role = 'Instructor' if course_id[1] == 'True' else 'Student'
            logger.debug(f"CreateInstructor: course_role: {course_role}")
            
            enrres = rest.enrollUserInCourse(course_id[0], "userName:" + instructor['userName'], course_role)

    if config['create_student']:
        
        student = rest.createLearnUser(create_user_json(data,False,password,config['student_role'],config['datasource'],config['student_convention']))
        
        login_info['student'] = student['userName']

        if "created_date" not in login_info:
            login_info['created_date'] = student['created']
        
        logger.debug("CreateStudent: course_ids: " + str(course_ids))
        
        for course_data in course_ids:
            course_id = course_data.split("^")
            logger.debug(f"CreateStudent: course_id: {course_id}")
            
            if len(course_id) > 1:
                logger.debug(f"CreateStudent: course_id[3]: {course_id[3]}")            
                if course_id[3] == "True":
                    enrres = rest.enrollUserInCourse(course_id[0], "userName:" + student['userName'], 'Student')


    logger.debug("generate login_info")
    login_info['given_name'] = data['given_name']
    login_info['event_id'] = data['event_id']

    logger.debug(str(login_info))

    return login_info


def lambda_handler(event, context):
    logger.debug("process")
    logger.debug("Event: " + str(event))

    try:
        for record in event['Records']:
            body = record['body']

            logger.debug("Body: " + str(body))

            data = json.loads(body)
        
            event_id = data['event_id']

            config = get_config(event_id)
            logger.debug("config: " + str(config))
            
            login_info = executeRegistration(data, event_id, config)
    
            logger.debug(str(login_info))

            sqs.send_message(
                QueueUrl=EMAIL_QUEUE_URL,
                MessageBody=(
                    json.dumps(login_info)
                )
            )

        # Delete received message from queue
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=record['receiptHandle']
            )
    except Exception as e:
        logger.error("Error processing registration: " + str(e))
        exit()