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

from pathlib import Path

import os
import snowflake.connector
import pandas as pd

class snowflake_controller():

    def __init__(self):
        
        cache_filename = f"file:///tmp/sfcache.txt"
        
        self.ctx = snowflake.connector.connect(
            user=os.environ['SNOWFLAKE_USER'],
            password=os.environ['SNOWFLAKE_PASS'],
            account=os.environ['SNOWFLAKE_ACCOUNT'],
            warehouse=os.environ['SNOWFLAKE_WH'],
            database=os.environ['SNOWFLAKE_DB'],
            ocsp_response_cache_filename=cache_filename
        )
        print("Got connection")

    def generate_username_from_email(self,email):
        
        print(f"username is {email.replace('.', '_').replace('@','_')}")
        return email.replace('.', '_').replace('@','_')
    
    def load_sql_file(self, filename):
        print(f"filename is {filename}.sql")
        
        return Path(f"{filename}.sql")
        
    def get_data(self,query,user_info):
        sql = self.load_sql_file(query).read_text()
        
        print(f"user_info is {user_info}")

        for key, value in user_info.items():
            print(f"key {key}, value {value}")
            sql = sql.replace('{' + key + '}', value)
        
        print(f"sql is {sql}")
        
        data = pd.read_sql(sql, self.ctx)
            
        print(data)
        
        return data    

    def create_snowflake_user(self,user_info):
        cur = self.ctx.cursor()
        print("reading text from sql file")
        
        try:
            create_user = self.get_data('create_user', user_info)
            print(f"create_user is {create_user}")
            alter_user = self.get_data('alter_user', user_info)
            print(f"alter_user is {alter_user}")
            grant_role = self.get_data('grant_role', user_info)
            print(f"grant_role is {grant_role}")
        
        
        finally:
            cur.close()
            
        self.ctx.close()