from constructs import Construct
from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    aws_applicationautoscaling as appscaling,
    CfnTag,
    Duration
)
from config import constants

class SentimentEndpointStack(Stack):
    """
    AWS CDK Stack to create a SageMaker endpoint with autoscaling.

    This stack creates a SageMaker model, endpoint configuration, and endpoint. It also sets up
    an autoscaling policy to scale the endpoint based on usage.

    Methods:
    __init__(scope: Construct, id: str, **kwargs): Initializes the SentimentEndpointStack.
    """
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        """
        Initializes the SentimentEndpointStack.

        Parameters:
        scope (Construct): The scope in which this stack is defined.
        id (str): The unique identifier for this stack.
        kwargs (dict): Additional keyword arguments for stack configuration.
        """
        ssm_parameter_model_s3 = kwargs.pop('ssm_parameter_model_s3')
        mode_image = kwargs.pop('mode_image')
        model_instance = kwargs.pop('model_instance')
        tags = kwargs.pop('tags')
        
        super().__init__(scope, id, **kwargs)

        model = sagemaker.CfnModel(self, "SentimentModel",
            model_name=ssm_parameter_model_s3,
            primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                image=mode_image,
                model_data_url="s3://sentiment-model"
            )
        )

        endpoint_config = sagemaker.CfnEndpointConfig(self, "EndpointConfig",
            production_variants=[sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                instance_type=model_instance,
                initial_instance_count=1,
                model_name=model.attr_model_name,
                variant_name="AllTraffic"
            )]
        )

        endpoint = sagemaker.CfnEndpoint(self, "Endpoint",
            endpoint_config_name=endpoint_config.get_att("EndpointConfigName").to_string(),  
            tags=[CfnTag(
                key=tags['key'],
                value=tags['value']
            )]
        )

        scaling_target = appscaling.ScalableTarget(self, "ScalingTarget",
            service_namespace=appscaling.ServiceNamespace.SAGEMAKER,
            max_capacity=5,
            min_capacity=1,
            resource_id=f"endpoint/{endpoint.endpoint_name}/variant/AllTraffic",
            scalable_dimension="sagemaker:variant:DesiredInstanceCount"
        )

        scaling_policy = appscaling.TargetTrackingScalingPolicy(self, "ScalingPolicy",
            scaling_target=scaling_target,
            target_value=constants.TARGET_VALUE,
            predefined_metric=appscaling.PredefinedMetric.SAGEMAKER_VARIANT_INVOCATIONS_PER_INSTANCE,
            scale_in_cooldown=Duration.seconds(constants.SCALEINCOOLDOWN),
            scale_out_cooldown=Duration.seconds(constants.SCALEOUTCOOLDOWN)
        )