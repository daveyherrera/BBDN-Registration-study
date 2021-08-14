import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="registration_service",
    version="0.0.1",

    description="A registration service integrated with Blackboard Learn for creating users, courses, and enrollments",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Scott Hurrey",

    package_dir={"": "registration_service"},
    packages=setuptools.find_packages(where="registration_service"),

    install_requires=[
        "aws-cdk.core==1.101.0",
        "aws-cdk.aws-lambda",
        "aws-cdk.aws_apigateway",
        "aws-cdk.aws-apigatewayv2",
        "aws-cdk.aws-apigatewayv2-integrations",
        "aws-cdk.aws-dynamodb",
        "aws-cdk.aws-s3",
        "aws-cdk.aws-s3-deployment",
        "aws-cdk.aws-s3-assets",
        "aws-cdk.aws-route53",
        "aws-cdk.aws-route53-targets",
        "aws-cdk.aws-certificatemanager",
        "aws-cdk.custom-resources",
        "aws-cdk.aws-iam",
        "aws-cdk.aws-sqs",
        "aws-cdk.aws-lambda-event-sources",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-elasticache",
        "aws-cdk.aws-events",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-lambda-python"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
