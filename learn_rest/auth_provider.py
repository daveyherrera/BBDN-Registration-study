import base64
import datetime
import json
import logging
import os
import ssl
import sys
import time
import urllib3
import urllib.parse

class auth_provider():
    target_url = ''

    def __init__(self, hostname):
        
        self.KEY = os.environ['REST_KEY']
        self.SECRET = os.environ['REST_SECRET']
        
        authstr = self.KEY + ':' + self.SECRET
        authstr_bytes = authstr.encode('UTF-8')
        authstr_encoded = base64.b64encode(authstr_bytes)
        
        self.HEADERS = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + authstr_encoded.decode('UTF-8')
        }

        self.BODY='grant_type=client_credentials'

        self.TOKEN = None
        self.target_url = hostname

        self.verify_certs = True
        
        self.http = urllib3.PoolManager()

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

        
    def getKey(self):
        return self.KEY

    def getSecret(self):
        return self.SECRET

    def test_token(self,token):
        REST_URL = 'https://' + self.target_url + '/learn/api/public/v1/system/version'
        
        self.logger.debug("REST_URL: " + REST_URL)
        
        # Authenticate
        r = self.http.request("GET", REST_URL, headers={ 'Authorization' : 'Bearer ' + token})

        if r.status == 200:
            return True

        else:
            return False

    def requestBasicToken(self):
        OAUTH_URL = 'https://' + self.target_url + '/learn/api/public/v1/oauth2/token'
        
        self.logger.debug("OAUTH_URL: " + OAUTH_URL)
        self.logger.debug("HEADERS: " + str(self.HEADERS))
        self.logger.debug("BODY: " + self.BODY)
        
        # Authenticate
        r = self.http.request("POST", OAUTH_URL, body=self.BODY, headers=self.HEADERS)

        res = json.loads(r.data)
        if r.status == 200:
            parsed_json = json.loads(r.data)
            self.logger.debug("parsed_json: " + str(parsed_json))
            token = parsed_json['access_token']
            self.logger.debug("token: " + str(token))
            expires_in = int(parsed_json['expires_in'])
            self.logger.debug("expires_in: " + str(expires_in))

            return token

        else:
            self.logger.error("[auth:setToken()] ERROR http_status: " + str(r.status) + " r: " + str(r.data))
            return None