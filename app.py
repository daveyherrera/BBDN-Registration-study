#!/usr/bin/env python3
import os

from aws_cdk import core as cdk


from registration_service.registration_service_stack import RegistrationServiceStack


app = cdk.App()
RegistrationServiceStack(app, "RegistrationServiceStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),    
    #env=cdk.Environment(account='123456789012', region='us-east-1'),
)

app.synth()
