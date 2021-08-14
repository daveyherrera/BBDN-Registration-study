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
            return None

    def createCustomDataObject(self,parentId,email):
        host = self.getBaseUrl()

        if host is None:
            return None

        endpoint = host + f"/api/REST/2.0/data/customObject/{parentId}/instance"
        self.logger.debug(f"createCustomDataObject: Request URL: POST {endpoint}")

        local_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
        local_headers.update(self.headers)
        self.logger.debug(f"createCustomDataObject: local_headers: {local_headers}")
        
        body={
            "type": "CustomObjectData",
            "fieldValues": [
                {
                "id": "4384",
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