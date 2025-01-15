import aws_cdk as cdk
from aws_cdk import assertions
from cdk_exercise_stacks.s3 import S3Stack
from cdk_exercise_stacks.lambda_functions import LambdaStack
from config import constants

def test_s3_bucket_created():
    app = cdk.App()
    lambda_stack = LambdaStack(app, "lambda-stack")
    stack = S3Stack(app, "s3-stack", lambda_stack=lambda_stack)

    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": constants.S3_BUCKET_NAME  # Update to match the actual bucket name
    })

def test_s3_encryption_enabled():
    app = cdk.App()
    lambda_stack = LambdaStack(app, "lambda-stack")
    stack = S3Stack(app, "s3-stack", lambda_stack=lambda_stack)

    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketEncryption": {
            "ServerSideEncryptionConfiguration": [
                {
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }
    })


def test_s3_notification_lambda_created():
    app = cdk.App()
    lambda_stack = LambdaStack(app, "lambda-stack")
    s3_stack = S3Stack(app, "s3-stack", lambda_stack=lambda_stack)

    template_s3 = assertions.Template.from_stack(s3_stack)

    template_s3.has_resource_properties("Custom::S3BucketNotifications", props={})
