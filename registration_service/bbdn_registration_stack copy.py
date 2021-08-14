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
    aws_iam as iam
)

from Config import config as cfg

import os


class BbdnRegistrationStack(cdk.Stack):

    def checkIfDynamoDbExists( self, table_name ):

        table = _dynamo.Table.from_table_name (
            self, table_name,
            table_name=table_name
        )

        if table is not None:
            return table
        else:
            return None
        
    def checkIfS3BucketExists( self, bucket_id, bucket_name ):

        bucket = s3.Bucket.from_bucket_name (
            self, bucket_id,
            bucket_name=bucket_name
        )

        if bucket is not None:
            return bucket
        else:
            return None


    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # Define Lambda function
        registration_lambda = _lambda.Function(
            self, "RegistrationnHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='registration.lambda_handler',
            environment = {
                
            }
        )

        configuration_lambda = _lambda.Function(
            self, "ConfigHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='setup.lambda_handler',
            environment = {
                
            }
        )

        api_policy_document = iam.PolicyDocument()

        # Define API Gateway and HTTP API
        registration_api = _apigw2.HttpApi(
            self, 'RegistrationAPI'
        )

        # Set up proxy integrations
        registration_lambda_integration = _a2int.LambdaProxyIntegration(
            handler=registration_lambda,
        )

        registrationt_entity = registration_api.add_routes(
            path="/", 
            methods=[_apigw2.HttpMethod.POST], 
            integration=registration_lambda_integration
        )

        config_lambda_integration = _a2int.LambdaProxyIntegration(
            handler=configuration_lambda,
        )

        config_entity = registration_api.add_routes(
            path="/setup", 
            methods=[_apigw2.HttpMethod.ANY], 
            integration=config_lambda_integration
        )


        # Define dynamoDb table
        tempTable = self.checkIfDynamoDbExists("configTable")
        if tempTable is None:
            config_table = _dynamo.Table(
                self, id="configTable",
                table_name="configTable",
                partition_key=_dynamo.Attribute(name="Event", type=_dynamo.AttributeType.STRING),
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
        else:
            config_table = tempTable

        # Add the table name as an environment variable
        registration_lambda.add_environment("TABLE_NAME", config_table.table_name)
        configuration_lambda.add_environment("TABLE_NAME", config_table.table_name)

        # Give lambdas the ability to read and write to the database table
        config_table.grant_full_access(configuration_lambda)
        config_table.grant_read_data(registration_lambda)

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, 'BbDevConZone',
            hosted_zone_id=cfg['HOSTED_ZONE_ID'],
            zone_name=cfg['DOMAIN_NAME']
        )

        devcon_certificate = acm.Certificate(self, "DevConCertificate",
            domain_name="*." + cfg['DOMAIN_NAME'],
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        api_domain = _apigw2.DomainName (
            self,'APIDomain',
            certificate=devcon_certificate,
            domain_name="api." + cfg['DOMAIN_NAME']
        )

        s3_domain = _apigw2.DomainName (
            self,'S3Domain',
            certificate=devcon_certificate,
            domain_name="registration." + cfg['DOMAIN_NAME']
        )

        reg_api_arecord = route53.ARecord(
            self, "AliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                alias.ApiGatewayv2Domain(api_domain)
            )
        )

        bucket_id = "RegistrationWebsite"
        bucket_name = "registration." + cfg['DOMAIN_NAME']
        
        tempBucket = self.checkIfS3BucketExists(bucket_id, bucket_name)
        
        if tempBucket is None:
            registration_website = s3.Bucket(self, bucket_id,
                bucket_name=bucket_name,
                public_read_access=True,
                website_index_document="index.html"
            )
        else:
            registration_website = tempBucket

        reg_asset_grant = registration_website.grant_public_access()
        config_lambda_grant = registration_website.grant_read_write(configuration_lambda)

        registration_website_files = s3deploy.BucketDeployment(
            self, 'DeployWebsite', 
            sources=[ s3deploy.Source.asset('./registration_site')], 
            destination_bucket=registration_website
        )

        route53.ARecord(self, "RegPageRecord",
            zone=hosted_zone,
            record_name="registration", # www
            target=route53.RecordTarget.from_alias(alias.BucketWebsiteTarget(registration_website))
        )

        
