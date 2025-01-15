import aws_cdk as cdk
import aws_cdk.assertions as assertions

from cdk_exercise_stacks.lambda_functions import LambdaStack
from config import constants


def test_lambda_created():
    app = cdk.App()

    lambda_stack = LambdaStack(app, "lambda-stack")

    template = assertions.Template.from_stack(lambda_stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": constants.LAMBDA_HANDLER,
        "FunctionName": constants.LAMBDA_NAME,
        "Runtime": constants.LAMBDA_RUNTIME,
        "Timeout": 60,
        "Environment": {
            "Variables": constants.LAMBDA_ENVIRONMENT_VARIABLE
        }
    })

def test_lambda_environment_variables():
    app = cdk.App()

    lambda_stack = LambdaStack(app, "lambda-stack")

    template = assertions.Template.from_stack(lambda_stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Environment": {
            "Variables":  constants.LAMBDA_ENVIRONMENT_VARIABLE
        }
    })

def test_lambda_role_created():
    app = cdk.App()

    lambda_stack = LambdaStack(app, "lambda-stack")

    lambda_template = assertions.Template.from_stack(lambda_stack)

    lambda_template.has_resource_properties("AWS::IAM::Role", {
        "ManagedPolicyArns": [
            {
                "Fn::Join": [
                    "",
                    [
                        "arn:",
                        {
                            "Ref": "AWS::Partition"
                        },
                        ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
                    ]
                ]
            }
        ]
    })

def test_lambda_policy_created():
    app = cdk.App()

    lambda_stack = LambdaStack(app, "lambda-stack")

    lambda_template = assertions.Template.from_stack(lambda_stack)

    lambda_template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": [
                        "ssm:PutParameter",
                        "cloudwatch:PutMetricData"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ],
            "Version": "2012-10-17"
        }
    })