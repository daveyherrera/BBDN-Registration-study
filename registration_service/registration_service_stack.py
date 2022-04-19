#!/usr/bin/env python3
from aws_cdk import (
    core as cdk, 
    aws_lambda as _lambda, 
    aws_apigateway as _apigw, 
    aws_apigatewayv2 as _apigw2, 
    aws_apigatewayv2_integrations as _a2int,
    aws_dynamodb as _dynamo,
    custom_resources as _resources,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_assets as s3assets,
    aws_route53 as route53,
    aws_route53_targets as alias,
    aws_certificatemanager as acm,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_lambda_event_sources as ales,
    aws_ec2 as ec2,
    aws_elasticache as cache,
    aws_events as events,
    aws_events_targets as event_targets,
    aws_lambda_python as lambpy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins
)

from Config import config
from Config import smtp
from Config import sfconfig

import os
import csv


class RegistrationServiceStack(cdk.Stack):

    def get_initial_data(self):

        with open('reg_config.csv') as csvfile:
            dataset = csv.DictReader(csvfile)
        
            data = []

            for row in dataset:
                data.append({
                    'Event': { 'S': row['Event'] },
                    'HostName': { 'S': row['HostName'] },
                    'CreateInstructor': { 'BOOL': bool(row['CreateInstructor'] == "True") },
                    'InstructorRole': { 'S': row['InstructorRole'] },
                    'CreateStudent': { 'BOOL': bool(row['CreateStudent'] == "True") },
                    'StudentRole': { 'S': row['StudentRole'] },
                    'StudentConvention': { 'S': row['StudentConvention'] },
                    'CourseIds': { 'S': row['CourseIds'] },
                    'IsTemplate': { 'BOOL': bool(row['IsTemplate'] == "True") },
                    'IsEloqua': { 'BOOL': bool(row['IsEloqua'] == "True") },
                    'EmailFrom': { 'S': row['EmailFrom'] },
                    'Datasource': { 'S': row['Datasource'] },
                    'EmailSubject': { 'S': row['EmailSubject'] },
                    'EventName': { 'S': row['EventName'] },
                    'EloquaCDOParentId': { 'S': row['EloquaCDOParentId'] },
                    'IsHubilo': { 'BOOL': bool(row['IsHubilo'] == "True") },
                    'HubiloId': { 'S': row['HubiloId'] },
                    'EloquaCDOFieldId': { 'S': row['EloquaCDOFieldId'] }
                })
        
        return data


    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        log_level = config['LOG_LEVEL']

        dead_letter_queue = sqs.DeadLetterQueue (
            max_receive_count=25,
            queue=sqs.Queue(
                    self, "DeadLetterQueue"
                )
        )

        registration_queue = sqs.Queue (
            self, "RegistrationQueue",
            visibility_timeout=cdk.Duration.minutes(15),
            dead_letter_queue=dead_letter_queue
        )

        hubilo_queue = sqs.Queue (
            self, "HubiloQueue",
            visibility_timeout=cdk.Duration.minutes(15),
            dead_letter_queue=dead_letter_queue
        )

        email_queue = sqs.Queue (
            self, "EmailQueue",
            visibility_timeout=cdk.Duration.minutes(15),
            dead_letter_queue=dead_letter_queue
        )
        
        snowflake_queue = sqs.Queue (
            self, "SnowflakeQueue",
            visibility_timeout=cdk.Duration.minutes(15),
            dead_letter_queue=dead_letter_queue
        )

        # Define dynamoDb table
        config_table = _dynamo.Table(
            self, id="configTable",
            table_name="configTable",
            partition_key=_dynamo.Attribute(name="Event", type=_dynamo.AttributeType.STRING),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            encryption=_dynamo.TableEncryption.AWS_MANAGED
        )
        
        # Set up the custom resource policy so we can populate the database upon creation
        policy = _resources.AwsCustomResourcePolicy.from_sdk_calls(
            resources=['*']
        )

        # Get the data to be added to the new table
        data = self.get_initial_data()

        # Create and execute custom resources to add data to the new table
        for i in range(0,len(data)):
            acronym_resource = _resources.AwsCustomResource (
                self, 'initDBResource' + str(i), 
                policy=policy,
                on_create=_resources.AwsSdkCall(
                    service='DynamoDB',
                    action='putItem',
                    parameters={ 'TableName': config_table.table_name, 'Item': data[i] },
                    physical_resource_id=_resources.PhysicalResourceId.of('initDBData' + str(i)),
                ),
            )

        snowflake_lambda_layer = lambpy.PythonLayerVersion (
            self, 'SnowflakeLambdaLayer',
            entry='snowflake-connector-python',
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
            description='Snowflake connector lambda layer',
            layer_version_name='SnowflakeLambdaLayer'
        )
               
        # Define Lambda function
        registration_lambda = _lambda.Function(
            self, "RegistrationHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/registration'),
            handler='registration.lambda_handler',
            environment = {
                'QUEUE_URL': registration_queue.queue_url,
                'HUBILO_QUEUE_URL': hubilo_queue.queue_url,
                'TABLE_NAME': config_table.table_name,
                'LOG_LEVEL' : log_level 
            },
        )

        api_lambda = _lambda.Function(
            self, "APIHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/api'),
            handler='api.lambda_handler',
            timeout=cdk.Duration.minutes(15),
            layers=[
                snowflake_lambda_layer
            ],
            environment = {
                'REST_KEY' : config['REST_KEY'],
                'REST_SECRET' : config['REST_SECRET'],
                'TABLE_NAME': config_table.table_name,
                'LOG_LEVEL' : log_level,
                'SNOWFLAKE_USER': sfconfig['user'],
                'SNOWFLAKE_PASS': sfconfig['password'],
                'SNOWFLAKE_ACCOUNT': sfconfig['account'],
                'SNOWFLAKE_WH': sfconfig['warehouse'],
                'SNOWFLAKE_DB': sfconfig['database'],
                'SNOWFLAKE_SCHEMA': sfconfig['schema']
            },
        )

        process_lambda = lambpy.PythonFunction(
            self, "ProcessHandler",
            entry="lambda/process",
            index="process.py",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler",
            timeout=cdk.Duration.minutes(15),
            environment = {
                'QUEUE_URL': registration_queue.queue_url,
                'EMAIL_QUEUE_URL': email_queue.queue_url,
                'SNOWFLAKE_QUEUE_URL': snowflake_queue.queue_url,
                'REST_KEY' : config['REST_KEY'],
                'REST_SECRET' : config['REST_SECRET'],
                'TABLE_NAME': config_table.table_name,
                'LOG_LEVEL' : log_level
            },
            events=[
                ales.SqsEventSource(registration_queue)
            ],
        )

        hubilo_lambda = _lambda.Function(
            self, "HubiloHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/hubilo'),
            handler='hubilo.lambda_handler',
            timeout=cdk.Duration.minutes(15),
            environment = {
                'QUEUE_URL': hubilo_queue.queue_url,
                'HUBILO_TOKEN' : config['HUBILO_TOKEN'],
                'TABLE_NAME': config_table.table_name,
                'LOG_LEVEL' : log_level,
                'SMTP_KEY': smtp['key'],
                'SMTP_SECRET' : smtp['secret']
            },
            events=[
                ales.SqsEventSource(hubilo_queue)
            ],
        )

        email_lambda = _lambda.Function(
            self, "EmailHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/email'),
            handler='email.lambda_handler',
            timeout=cdk.Duration.minutes(15),
            environment = {
                'SMTP_KEY': smtp['key'],
                'SMTP_SECRET' : smtp['secret'],
                'SMTP_SENDER_ADDRESS' : smtp['sender'],
                'SMTP_SENDER_NAME' : smtp['sender_name'],
                'SMTP_HOST' : smtp['host'],
                'SMTP_PORT' : smtp['port'],
                'EMAIL_QUEUE_URL': email_queue.queue_url,
                'TABLE_NAME': config_table.table_name,
                'LOG_LEVEL' : log_level
            },
            events=[
                ales.SqsEventSource(email_queue)
            ],
        )

        authorization_lambda = _lambda.Function(
            self, "AuthHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/authorizer'),
            handler='authorizer.lambda_handler',
            environment = {
                'IP_WHITELIST': config['IP_WHITELIST'],
                'LOG_LEVEL' : log_level
            }
        )

        trial_cleanup_lambda = lambpy.PythonFunction(
            self, "CleanUpHandler",
            entry="lambda/cleanup",
            index="cleanup.py",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler",
            timeout=cdk.Duration.minutes(15),
            environment = {
                'REST_KEY' : config['REST_KEY'],
                'REST_SECRET' : config['REST_SECRET'],
                'TABLE_NAME': config_table.table_name,
                'LOG_LEVEL' : log_level
            }
        )

        
        # Give lambdas the ability to read and write to the database table
        config_table.grant_read_data(authorization_lambda)
        config_table.grant_read_data(registration_lambda)
        config_table.grant_read_data(process_lambda)
        config_table.grant_read_data(api_lambda)
        config_table.grant_read_data(email_lambda)
        config_table.grant_read_data(hubilo_lambda)
        config_table.grant_read_data(trial_cleanup_lambda)
        
        registration_queue.grant_send_messages(registration_lambda)
        hubilo_queue.grant_send_messages(registration_lambda)
        email_queue.grant_send_messages(process_lambda)
        snowflake_queue.grant_send_messages(process_lambda)

        #setup free trial cleanup
        trial_cleanup_schedule = events.Schedule.rate(cdk.Duration.days(1))

        trial_cleanup_lambda_target = event_targets.LambdaFunction(handler=trial_cleanup_lambda)

        lambda_cw_event = events.Rule(
            self, "TrialCleanupRule",
            description=
            "Trigger the Trial cleanup lambda once per day to remove accounts older than 30 days",
            enabled=True,
            schedule=trial_cleanup_schedule,
            targets=[trial_cleanup_lambda_target]
        )

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, 'BbDevConZone',
            hosted_zone_id=config['HOSTED_ZONE_ID'],
            zone_name=config['DOMAIN_NAME']
        )

        devcon_certificate = acm.Certificate(self, "DevConCertificate",
            domain_name="registration." + config['DOMAIN_NAME'],
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        registration_domain = _apigw2.DomainName (
            self,'RegDomain',
            certificate=devcon_certificate,
            domain_name="registration." + config['DOMAIN_NAME']
        )

        reg_api_arecord = route53.ARecord(
            self, "AliasRecord",
            zone=hosted_zone,
            record_name="registration",
            target=route53.RecordTarget.from_alias(
                alias.ApiGatewayv2DomainProperties(registration_domain.regional_domain_name,registration_domain.regional_hosted_zone_id)
            )
        ) 

        bde_certificate = acm.Certificate(self, "BDECertificate",
            domain_name="bde." + config['DOMAIN_NAME'],
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        bde_domain = _apigw2.DomainName (
            self,'BDEDomain',
            certificate=bde_certificate,
            domain_name="bde." + config['DOMAIN_NAME']
        )

        # Set up proxy integrations
        registration_lambda_integration = _a2int.LambdaProxyIntegration(
            handler=registration_lambda,
        )

        api_lambda_integration = _a2int.LambdaProxyIntegration(
            handler=api_lambda,
        )

        # Define API Gateway and HTTP API
        registration_api = _apigw2.HttpApi(
            self, 'RegistrationAPI',
            default_integration=registration_lambda_integration,
            default_domain_mapping={
                "domain_name": registration_domain
            }
        )

        registration_authorizer_arn = 'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/' + authorization_lambda.function_arn + '/invocations'

        registration_authorizer = _apigw2.CfnAuthorizer(
            self, "RegistrationAuthorizer", 
            api_id=registration_api.api_id,
            authorizer_type='REQUEST', 
            identity_source=['$context.identity.sourceIp'],
            name="RegistrationAuthorizer",
            authorizer_uri=registration_authorizer_arn,
            authorizer_result_ttl_in_seconds=3600,
            authorizer_payload_format_version='2.0',
            enable_simple_responses=True
        )

        permission = _lambda.CfnPermission(
            self, 'AuthorizerInvokePermission',
            action="lambda:InvokeFunction",
            principal="apigateway.amazonaws.com",
            function_name=authorization_lambda.function_name,
            source_arn=cdk.Arn.format(
                stack=self,
                components=cdk.ArnComponents(service="execute-api",
                    resource=registration_api.api_id,
                    resource_name="authorizers/" + registration_authorizer.ref
                )
            )
        )

        cdk.CfnOutput(self, "API Endpoint", value=registration_api.api_endpoint)
        cdk.CfnOutput(self, "Default Stage", value=str(registration_api.default_stage.to_string()))
        cdk.CfnOutput(self, "URL", value=registration_api.url)

        registration_entity = _apigw2.HttpRoute(
            self, "RegistrationRoute",
            http_api=registration_api,
            route_key=_apigw2.HttpRouteKey.with_('/register', _apigw2.HttpMethod.ANY),
            integration=registration_lambda_integration
        )

        routeCfn = registration_entity.node.default_child
        routeCfn.authorizer_id = registration_authorizer.ref
        routeCfn.authorization_type = "CUSTOM"

        api_entity = _apigw2.HttpRoute(
            self, "APIRegistrationRoute",
            http_api=registration_api,
            route_key=_apigw2.HttpRouteKey.with_('/api', _apigw2.HttpMethod.POST),
            integration=api_lambda_integration
        )

        bde_bucket = s3.Bucket(self, "bde-registration",
            bucket_name="bde-registration"
        )

        bde_website_files = s3deploy.BucketDeployment(
            self, 'DeployWebsite', 
            sources=[ s3deploy.Source.asset('./bde_registration_site')], 
            destination_bucket=bde_bucket
        )

        bde_cf_distribution = cloudfront.Distribution(self, "BDEDistro",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bde_bucket),
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=["bde.bbdevcon.com"],
            default_root_object="index.html",
            certificate=bde_certificate,
            enable_logging=True
        )

        bde_api_arecord = route53.ARecord(
            self, "BDEAliasRecord",
            zone=hosted_zone,
            record_name="bde",
            target=route53.RecordTarget.from_alias(
                alias.CloudFrontTarget(bde_cf_distribution)
            )
        ) 


