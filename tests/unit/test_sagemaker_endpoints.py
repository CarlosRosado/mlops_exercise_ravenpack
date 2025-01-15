from aws_cdk import assertions
from aws_cdk import App
from cdk_exercise_stacks.sagemaker_endpoints import SentimentEndpointStack
from config import constants


def test_sagemaker_endpoint_created():
    app = App()
    stack = SentimentEndpointStack(app, "sagemaker-endpoint-stack",
                                   ssm_parameter_model_s3=constants.SSM_PARAMETER_MODEL,
                                   mode_image=constants.SAGEMAKER_MODEL_IMAGE,
                                   model_instance=constants.SAGEMAKER_INSTANCE_TYPE,
                                   tags={'key': 'key', 'value': 'value'})

    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SageMaker::Endpoint", {
        "EndpointConfigName": {
            "Fn::GetAtt": ["EndpointConfig", "EndpointConfigName"]
        },
        "Tags": [
            {
                "Key": "key",
                "Value": "value"
            }
        ]
    })

def test_sagemaker_endpoint_config_created():
    app = App()
    stack = SentimentEndpointStack(app, "sagemaker-endpoint-stack",
                                   ssm_parameter_model_s3=constants.SSM_PARAMETER_MODEL,
                                   mode_image=constants.SAGEMAKER_MODEL_IMAGE,
                                   model_instance=constants.SAGEMAKER_INSTANCE_TYPE,
                                   tags={'key': 'key', 'value': 'value'})

    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SageMaker::EndpointConfig", {
        "ProductionVariants": [
            {
                "InstanceType": constants.SAGEMAKER_INSTANCE_TYPE,
                "InitialInstanceCount": 1,
                "ModelName": {
                    "Fn::GetAtt": ["SentimentModel", "ModelName"]
                },
                "VariantName": "AllTraffic"
            }
        ]
    })

    
def test_sentiment_model_created():
    app = App()
    stack = SentimentEndpointStack(app, "sagemaker-endpoint-stack",
                                   ssm_parameter_model_s3=constants.SSM_PARAMETER_MODEL,
                                   mode_image=constants.SAGEMAKER_MODEL_IMAGE,
                                   model_instance=constants.SAGEMAKER_INSTANCE_TYPE,
                                   tags={'key': 'key', 'value': 'value'})

    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SageMaker::Model", {
        "ModelName": constants.SSM_PARAMETER_MODEL,
        "PrimaryContainer": {
            "Image": constants.SAGEMAKER_MODEL_IMAGE,
            "ModelDataUrl": "s3://sentiment-model"
        }
    })

def test_autoscaling_policy_created():
    app = App()
    stack = SentimentEndpointStack(app, "sagemaker-endpoint-stack",
                                   ssm_parameter_model_s3=constants.SSM_PARAMETER_MODEL,
                                   mode_image=constants.SAGEMAKER_MODEL_IMAGE,
                                   model_instance=constants.SAGEMAKER_INSTANCE_TYPE,
                                   tags={'key': 'key', 'value': 'value'})

    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::ApplicationAutoScaling::ScalingPolicy", {
        "PolicyName": "sagemakerendpointstackScalingPolicy45E98274",
        "PolicyType": "TargetTrackingScaling",
        "ScalingTargetId": { "Ref": "ScalingTargetE4877F50" },
        "TargetTrackingScalingPolicyConfiguration": {
            "ScaleInCooldown": constants.SCALEINCOOLDOWN,
            "ScaleOutCooldown": constants.SCALEOUTCOOLDOWN,
            "TargetValue": constants.TARGET_VALUE,
            "PredefinedMetricSpecification": {
                "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
            }
        }
    })