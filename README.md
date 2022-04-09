
# BBDN Registration Service

This project is a servless application to handle event registrations. It is commonly used for two purposes:
* Registration for events in Hubilo
* Registration for programs hosted in Blackboard Learn

It includes an HTTP API Gateway for handling incoming requests, a [chain of Lambdas and SQS queues](docs/workflow.md) to handle the various work flows, and a [DynamoDb](docs/schema.md) table to store configuration. Most of the time, adding a new event is done by adding a row to the DynamoDb table.

## How it works

1. The entry point to the service is the HTTP API Gateway. It takes an HTTP POST, validates that is a trusted post, and then forwards the POST to the registration Lambda. 
2. The registration lambda decrypts the post parameters and validates that it is for a valid event. Assuming it is, it then determines which branch it belongs in, creates and SQS event, and posts it to the appropriate queue
3. Posting to the queue triggers the next set of lambdas to process the event. If it is Hubilo, it is picked up by that lambda, if it is Learn, it is picked up by the process lambda.
4. In cases where email must be sent, the lambda will package the information that needs to be send into an SQS event and puts it on the email queue. 
5. The email lambda picks up the package, generates and Eloqua email, and sends it through the Eloqua API. 

## How to Configure

There are two files used to configure the app. The most important is ConfigTemplate.py. Copy this file to Config.py and add your information. These files are not deployed, but rather feed CDK this information to be deployed using environment variables accessible to the lambdas that require them.

*Config* - used to configure the application itself

| Key | Value | Notes |
| --- | --- | --- |
| 'HOSTED_ZONE_ID' | 'Route53HostedZoneId' | assumes your route53 is pre-configured |
| 'DOMAIN_NAME' | 'Route53DomainName' | assumes your route53 is pre-configured |
| 'ACCOUNT' | 'AwsAccountNumber' | the account number for the aws account you are deploying to |
| 'REGION' | 'us-east-1' | |
| 'REST_KEY' | 'LearnRestKey' | retreived from the developer portal |
| 'REST_SECRET' | 'LearnRestSecret' | retreived from the developer portal |
| 'IP_WHITELIST' | 'SourceIpsDelimetedWith\|' | the IP Addresses you will accept HTTP POSTs from |
| 'LOG_LEVEL' | 'DEBUG' | |
| 'HUBILO_TOKEN' | 'HubiloTokenId' | Provided by Hubilo |

*SMTP* - used to configure the Eloqua email

| Key | Value | Notes |
| --- | --- | --- |
| "key" | "EloquaLogin" | Provided by marketing |
| "secret" | "EloquaPassword" | Provided by marketing |
| "sender" | "SenderEmail" | Default value almost always overwritten in the event config |
| "sender_name" | "SenderName" | Default value almost always overwritten in the event config |
| "host" | "SmtpHost" | Default value almost always overwritten in the event config |
| "port" | "SmtpPort" | Default value almost always overwritten in the event config |

The next file in question is a mechanism to populate the dynamo config table the first time to deploy the stack. If the stack is already deployed, this file has no effect. 

## How to Deploy

This project is deployed using the AWS Cloud Development Kit, or CDK. 

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
