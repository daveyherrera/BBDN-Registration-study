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


import os
import snowflake.connector
import pandas as pd

class snowflake_controller():

    def __init__(self):
        self.ctx = snowflake.connector.connect(
            user=os.environ['SNOWFLAKE_USER'],
            password=os.environ['SNOWFLAKE_PASS'],
            account=os.environ['SNOWFLAKE_ACCOUNT'],
            warehouse=os.environ['SNOWFLAKE_WH'],
            database=os.environ['SNOWFLAKE_DB']
        )

    def generate_username_from_email(self,email):
        return email.replace('.', '_').replace('@','_')
    
    def load_sql_file(self, filename):
        return f"{filename}.sql"

    def create_snowflake_user(self,user_info):
        cur = self.ctx.cursor()
        sql = self.load_sql_file('create_user').read_text()

        for key, value in user_info.items():
            sql = sql.replace('{' + key + '}', value)
        
        try:
            data = pd.read_sql(sql, self.ctx)
            
            print(data)
        
        finally:
            cur.close()
            
        self.ctx.close()