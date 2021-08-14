import base64
import json
from eloqua import eloqua_controller
import logging
import os
import smtplib 
import urllib3

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

import email_block
import eloqua

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')

QUEUE_URL = os.environ['EMAIL_QUEUE_URL']
TABLE_NAME = os.environ['TABLE_NAME']

table = dynamodb.Table(TABLE_NAME)

http = urllib3.PoolManager()

KEY = os.environ['SMTP_KEY']
SECRET = os.environ['SMTP_SECRET']

http_auth = KEY + ':' + SECRET
headers = urllib3.make_headers(basic_auth=http_auth)

TOKEN = ""

sender = os.environ['SMTP_SENDER_ADDRESS']
sender_name = os.environ['SMTP_SENDER_NAME']

id = ""
user_id = ""

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

eloqua_controller = eloqua_controller(headers)

def get_config(event_id):

    results = table.query(KeyConditionExpression=Key("Event").eq(event_id))
    
    config = {}
    
    try:
        item = results['Items'][0]
        logger.debug("item: " + str(item))
        
        config['hostname'] = item['HostName']
        logger.debug("config['hostname']: " + str(config['hostname']))
        config['is_eloqua'] =  item['IsEloqua']
        logger.debug("config['is_eloqua']: " + str(config['is_eloqua']))
        config['email_from'] =  item['EmailFrom']
        logger.debug("config['email_from']: " + str(config['email_from']))
        config['email_subject'] = item['EmailSubject']
        logger.debug("config['email_subject']: " + str(config['email_subject']))
        config['event_name'] = item['EventName']
        logger.debug("config['event_name']: " + str(config['event_name']))
        config['parent_id'] = item['EloquaCDOParentId']
        logger.debug("config['parent_id']: " + str(config['parent_id']))
        
    except Exception as e:
        logger.error(str(e))
        logger.error(event_id + ' is not defined.')

    return config

def getTextEmail(firstname, learn_url, instructor, student, password):
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        f"Dear {firstname}," 
        f""
        f"Thank you for registering for the Learn Trial Experience. Get ready to make the most of a unique learning experience. Save this e-mail as it contains instructions on how to start using your 30-day trial."
        f""
        f"How to access your 30-day Blackboard Learn Trial Experience?"
        f""
        f"Follow this instructions:"
        f"  - Login to this page: {learn_url}"
        f"  - Instructor Username: {instructor}"
        f"  - Student Username: {student}"
        f"  - Password: {password}"
        f""
        f"For more information about Blackboard Learn, please visit this site. https://www.blackboard.com/teaching-learning/learning-management/blackboard-learn"
        f"Need help? Please visit our Help Center. https://help.blackboard.com/Learn"
        f""
        f"Enjoy,"
        f"The Blackboard Team"
    )
    
    return BODY_TEXT
  
def lambda_handler(event,context):
    logger.debug("email")
    logger.debug("Event: " + str(event))

    host = eloqua_controller.getBaseUrl()
    
    logger.debug("host: " + host)
        

    try:
        for record in event['Records']:
            body = record['body']
            
            data = json.loads(body)
            logger.debug("Data: " + str(data))

            if 'user_exists' not in data:
                config = get_config(data['event_id'])

                emailBlock=email_block.EmailBlock()

                email = data['instructor']
                logger.debug("email: " + email)
                password = data['password']
                logger.debug("password: " + password)
                student = data['student']
                logger.debug("student: " + student)
                given_name = data['given_name']
                logger.debug("given_name: " + given_name)
                created_date = data['created_date']
                logger.debug("created_date: " + created_date)

                subject = config['email_subject']
                logger.debug("subject: " + subject)

                text_body = getTextEmail(given_name, config['hostname'], email, student, password)
                logger.debug("text_body: " + str(text_body))

                html_body = emailBlock.getEmailBlock(given_name, config['hostname'], email, student, password)
                logger.debug("html_body: " + str(html_body))

                email_body = eloqua_controller.createEmailBody(subject,html_body,text_body,config['email_from'],config['event_name'])
                logger.debug("email_body: " + str(email_body))
                
                user_id = eloqua_controller.getUserByEmail(host,email)
                
                email_id = eloqua_controller.createEmail(host,email_body)

                post_body = eloqua_controller.generatePostBody(subject,email_id,user_id)

                logger.debug(str(post_body))

                sent_email_id = eloqua_controller.sendMail(host,post_body)

                status_code = eloqua_controller.deleteEmail(host,email_id)

                eloqua_controller.createCustomDataObject(host,config['parent_id'],email,created_date)
                
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=record['receiptHandle']
            )

        return
    except Exception as e:
        logger.error("Error Processing Email: " + str(e))
        exit()
    