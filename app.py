#!/usr/bin/env python3
import aws_cdk as cdk
import config.constants as constants

from cdk_exercise_stacks.lambda_functions import LambdaStack
from cdk_exercise_stacks.s3 import S3Stack
from cdk_exercise_stacks.sagemaker_endpoints import SentimentEndpointStack


app = cdk.App()

lambda_stack = LambdaStack(app, "lambda-stack")
s3_stack = S3Stack(app, "s3-stack", lambda_stack=lambda_stack)
sagemaker_endpoint_stack = SentimentEndpointStack(app, "sagemaker-endpoint-stack",
                                                  ssm_parameter_model_s3=constants.SSM_PARAMETER_MODEL,
                                                  mode_image=constants.SAGEMAKER_MODEL_IMAGE,
                                                  model_instance=constants.SAGEMAKER_INSTANCE_TYPE,
                                                  tags={'key': 'key', 'value': 'value'})


app.synth()
