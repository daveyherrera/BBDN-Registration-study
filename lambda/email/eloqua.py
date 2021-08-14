import datetime
import json
import logging
import os
import ssl
import sys
import time
import urllib3
import urllib.parse


class eloqua_controller():

    def __init__(self, headers):
        
        self.headers = headers

        LOG_LEVEL = os.environ['LOG_LEVEL']
        self.logger = logging.getLogger()

        if LOG_LEVEL == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif LOG_LEVEL == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif LOG_LEVEL == "WARN":
            self.logger.setLevel(logging.WARN)
        else:
            self.logger.setLevel(logging.INFO)
        
        self.http = urllib3.PoolManager()

    def getBaseUrl(self):
        endpoint = 'https://login.eloqua.com/id'
        self.logger.debug("endpoint: " + str(endpoint))
        
        r = self.http.request("GET", endpoint, headers=self.headers)

        if r.status == 200:
            parsed_json = json.loads(r.data)
            
            self.logger.debug("parsed_json: " + str(parsed_json))
            
            id = parsed_json['site']['id']
            user_id = parsed_json['user']['id']

            self.logger.debug("[auth:setToken()] update: id=" + str(id) + " user_id=" + str(user_id) + " base_url=" + parsed_json['urls']['base'])

            return(parsed_json['urls']['base'])

        else:
            self.logger.error("[auth:setToken()] ERROR " + str(r.status) + " " + str(r.data))


    def getUserByEmail(self,host,email):

        endpoint = host + '/api/REST/2.0/data/contacts?search=emailAddress=' + email + '&count=1'
        self.logger.debug("endpoint: " + str(endpoint))

        # Authenticate
        print("[auth:setToken] GET Request URL: " + endpoint)
        
        r = self.http.request("GET", endpoint, headers=self.headers)

        print("[auth:setToken()] STATUS CODE: " + str(r.status) )
        #strip quotes from result for better dumps

        if r.status == 200:
            parsed_json = json.loads(r.data)
            
            self.logger.debug(parsed_json)

            uid = parsed_json['elements'][0]['id']

            self.logger.debug(str(uid))
            return(uid)

        else:
            self.logger.error("[auth:setToken()] ERROR " + str(r.status) + " " + str(r.data))

    def createEmail(self,host,post_body):
        endpoint = host + '/api/REST/2.0/assets/email'

        # Authenticate
        self.logger.debug("[auth:setToken] POST Request URL: " + endpoint)
        
        local_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }

        local_headers.update(self.headers)
        
        self.logger.debug(f"Headers: {local_headers} Post Body {post_body}")
        
        r = self.http.request("POST", endpoint, body=json.dumps(post_body), headers=local_headers)

        self.logger.debug("[auth:setToken()] STATUS CODE: " + str(r.status) )
        #strip quotes from result for better dumps

        if r.status == 201:
            parsed_json = json.loads(r.data)
            
            self.logger.debug(f"Email created: {parsed_json}")

            return(parsed_json['id'])

        else:
            self.logger.error("[auth:setToken()] ERROR " + str(r.status) + " " + str(r.data))

    def sendMail(self,host,post_body):
        endpoint = host + '/api/REST/2.0/assets/email/deployment'

        # Authenticate
        self.logger.debug("[auth:setToken] POST Request URL: " + endpoint)
        
        local_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }

        local_headers.update(self.headers)
        
        self.logger.debug(f"Headers: {local_headers} Post Body {post_body}")

        r = self.http.request("POST", endpoint, body=json.dumps(post_body), headers=local_headers)

        self.logger.debug("[auth:setToken()] STATUS CODE: " + str(r.status) )
        #strip quotes from result for better dumps

        if r.status == 200 or r.status == 201:
            parsed_json = json.loads(r.data)
            
            self.logger.debug(parsed_json)

            eid = parsed_json['id']

            self.logger.debug(str(eid))

            return(eid)

        else:
            self.logger.error("[auth:setToken()] ERROR " + str(r.status) + "\r\n")
            self.logger.error("headers: " + str(r.headers))
            self.logger.error("text: " + str(r.data))

        return(r.status)

    def deleteEmail(self,host,eid):
        endpoint = host + '/api/REST/2.0/assets/email/' + str(eid)

        # Authenticate
        self.logger.debug("[auth:setToken] DELETE Request URL: " + endpoint)
        
        r = self.http.request("DELETE", endpoint, headers=self.headers)

        self.logger.debug("[auth:setToken()] STATUS CODE: " + str(r.status) )
        #strip quotes from result for better dumps

        if r.status != 200:
            self.logger.error("[auth:setToken()] ERROR " + str(r.status) + " " + str(r.data))

        return r.status

    def createCustomDataObject(self,host,parentId,email,created_date):
        endpoint = host + f"/api/REST/2.0/data/customObject/{parentId}/instance"
        self.logger.debug(f"createCustomDataObject: Request URL: POST {endpoint}")

        local_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
        local_headers.update(self.headers)
        self.logger.debug(f"createCustomDataObject: local_headers: {local_headers}")
        
        body={
            "type": "CustomObjectData",
            "fieldValues": [
                {
                "id": "4381",
                "value": created_date
                },
                {
                "id": "4382",
                "value": email
                }
            ]
        }

        self.logger.debug(f"createCustomDataObject: Request Body: {body}")
        
        r = self.http.request("POST", endpoint, body=json.dumps(body), headers=local_headers)

        self.logger.debug("[auth:setToken()] STATUS CODE: " + str(r.status) )
        #strip quotes from result for better dumps

        if r.status != 200:
            self.logger.error("[auth:setToken()] ERROR " + str(r.status) + " " + str(r.data))

        return r.status
    
    def generatePostBody(self, subject, eId, uId):

        return({
            "type": "EmailTestDeployment",
            "name": subject,
            "contactId": str(uId),
            "email": {
                "type": "Email",
                "id": str(eId),
                "name": subject
            },
            "sendOptions": {
                "allowResend": "true",
                "allowSendToBounceback": "false",
                "allowSendToGroupUnsubscribe": "true",
                "allowSendToMasterExclude": "true",
                "allowSendToUnsubscribe": "true"
            }
        })

    def createEmailBody(self, subject, html_body, text_body, sender, sender_name):

        return({
            "name": "Registration",
            "encodingId": 1,
            "emailGroupId": 28,
            "htmlContent": {
                "type": "RawHtmlContent",
                "html": html_body
            },
            "isPlainTextEditable": False,  
            "name": subject,  
            "plainText": text_body,  
            "sendPlainTextOnly": False,  
            "subject": subject,
            "folderId": "35451",
            "replyToEmail": sender,
            "replyToName" : sender_name,
            "senderEmail" : sender,
            "senderName" : sender_name 

        })