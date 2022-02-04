import datetime
import json
import logging
import os
import ssl
import sys
import time
import urllib3
import urllib.parse

class rest_controller():
    target_url = ''

    def __init__(self, token, hostname, datasource=None):
        
        self.target_url = hostname
        self.datasource = datasource
        self.authStr = 'Bearer ' + token
        
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

    def userExists(self,email):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/users/userName:' + email

        r = self.http.request("GET", endpoint, headers={'Authorization':self.authStr})

        if r.status == 404:
            return False
        else:
            return True

    def createLearnUser(self,user):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/users'

        r = self.http.request("POST", endpoint, body=json.dumps(user), headers={'Authorization':self.authStr, 'Content-Type' : 'application/json'})

        if r.status == 201 and r.data:
            res = json.loads(r.data)
            self.logger.debug("createLearnUser [status: " + str(r.status) + " res: " + str(res) + "]")
            return(res)
        elif r.status == 409:
            res = json.loads({ "409" : True })
            return(res)
        else:
            self.logger.error("http_status " + str(r.status) + " result " + str(r.data))
            return({ "http_status" : str(r.status), "result" : str(r.data) })

    def enrollUserInCourse(self,courseId, userId, courseRoleId):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/courses/' + courseId + '/users/userName:' + userId

        self.logger.debug(f"enrollUserInCourse->endpoint {endpoint}")
        payload = {
            "availability": {
                "available": "Yes"
            },
            "courseRoleId": courseRoleId,
            "dataSourceId": self.datasource
        }
        
        self.logger.debug(f"enrollUserInCourse->payload {payload}")

        r = self.http.request("PUT", endpoint, body=json.dumps(payload), headers={'Authorization':self.authStr, 'Content-Type' : 'application/json'})
        
        self.logger.debug(f"enrollUserInCourse->r.status {r.status}")

        if r.status == 201 and r.data:
            res = json.loads(r.data)
            self.logger.debug("enrollUserInCourse [status: " + str(r.status) + " res: " + str(res) + "]")
            return(res)
        else:
            self.logger.error("http_status " + str(r.status) + " result " + str(r.data))
            return({ "http_status" : str(r.status), "result" : str(r.data) })

    def createCourseFromTemplate(self,template_id, new_course_id, datasource=None):
        OAUTH_URL = 'https://' + self.target_url + '/learn/api/public/v2/courses/' + template_id + '/copy'

        course_id = template_id.split(":")[1]

        payload = {
            "targetCourse": {
                "courseId": new_course_id
            }
        }

        r = self.http.request("POST", OAUTH_URL, body=json.dumps(payload), headers={'Authorization':self.authStr, 'Content-Type':'application/json'})

        if r.status == 202:
            location = 'https://' + self.target_url + r.headers['Location']
            
            self.logger.debug("location: " + location)
            
            while True:
                r = self.http.request("GET", location, headers={'Authorization':self.authStr})
                
                if r.data:
                    res = json.loads(r.data)
                    if 'uuid' in res:
                        self.logger.debug("createCourseFromTemplate [status: " + str(r.status) + " res: " + str(res) + "]")
                        course_id = res['id']
                        if datasource is not None:
                            self.updateDatasource(course_id,datasource)
                        return(course_id)
                
                time.sleep(1)
        
        self.logger.error("http_status " + str(r.status) + " result " + str(r.data))
        return({ "http_status" : str(r.status), "result" : str(r.data) })
    
    def updateDatasource(self,course_id, datasource):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v3/courses/' + course_id

        body = {
            'dataSourceId' : datasource
        }

        r = self.http.request("PATCH", endpoint, body=json.dumps(body), headers={'Authorization':self.authStr, 'Content-Type' : 'application/json'})

        if r.status == 200 and r.data:
            res = json.loads(r.data)
            self.logger.debug("updateDatasource [status: " + str(r.status) + " res: " + str(res) + "]")
            return(res)
        else:
            self.logger.error("http_status " + str(r.status) + " result " + str(r.data))
            return({ "http_status" : str(r.status), "result" : str(r.data) })

    def getDataSourceId(self,datasource):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/dataSources/' + datasource

        r = self.http.request("GET", endpoint, headers={'Authorization':self.authStr})

        if r.status == 200 and r.data:
            res = json.loads(r.data)
            self.logger.debug("getDataSourceId [status: " + str(r.status) + " res: " + str(res) + "]")
            return(res['id'])
        else:
            self.logger.error("http_status " + str(r.status) + " result " + str(r.data))
            return({ "http_status" : str(r.status), "result" : str(r.data) })

    def deleteExpiredUsers(self, datasourceId):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/users'

        dt = datetime.datetime.now() - datetime.timedelta(30)
        expiry_date = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.logger.debug('Current Date :' + str(datetime.datetime.now()))
        self.logger.debug("30 days before Current Date : " + expiry_date)

        endpoint += f"?created={expiry_date}&createdCompare=lessThan"

        got_more = True
        
        while got_more:

            r = self.http.request("GET", endpoint, headers={'Authorization':self.authStr})

            if r.status == 200 and r.data:
                res = json.loads(r.data)
                self.logger.debug("deleteExpiredUsers [status: " + str(r.status) + " res: " + str(res) + "]")
                
                for user in res['results']:
                    if user['dataSourceId'] == datasourceId:
                        delete_endpoint = 'https://' + self.target_url + '/learn/api/public/v1/users/' + user['id']
                        user_json = {
                            "availability": {
                                "available": "No"
                            }
                        }
                        r = self.http.request("PATCH", delete_endpoint, body=json.dumps(user_json), headers={'Authorization':self.authStr, 'Content-Type': 'application/json'})
                
                try:
                    endpoint = 'https://' + self.target_url + res['paging']['nextPage']
                    self.logger.debug("deleteExpiredUsers: nextPage=" + str(endpoint))
                except:
                    got_more = False
                    self.logger.info("deleteExpiredUsers: Done!")

            else:
                got_more = False
                self.logger.error("deleteExpiredUsers: http_status " + str(r.status) + " result " + str(r.data))
                return({ "deleteExpiredUsers: http_status" : str(r.status), "result" : str(r.data) })