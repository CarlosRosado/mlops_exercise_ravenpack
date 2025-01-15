from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration,
    Environment
)
from config import constants

class LambdaStack(Stack):
    """
    AWS CDK Stack to create a Lambda function with necessary permissions.

    This stack creates a Lambda function with the specified handler, runtime, environment variables,
    and timeout. It also attaches the necessary IAM policies to allow the function to interact with
    other AWS services such as SSM and CloudWatch.

    Methods:
    __init__(scope: Construct, id: str, **kwargs): Initializes the LambdaStack.
    """
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        """
        Initializes the LambdaStack.

        Parameters:
        scope (Construct): The scope in which this stack is defined.
        id (str): The unique identifier for this stack.
        kwargs (dict): Additional keyword arguments for stack configuration.
        """
        env = Environment(account="account-id", region="region")
        super().__init__(scope, id, env=env, **kwargs)

        self.lambda_function = _lambda.Function(self, "LambdaFunction",
            function_name=constants.LAMBDA_NAME,
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler=constants.LAMBDA_HANDLER,
            code=_lambda.Code.from_asset("resources/lambda"),
            environment=constants.LAMBDA_ENVIRONMENT_VARIABLE,
            timeout=Duration.seconds(60)  # Set the timeout
        )

        self.lambda_function.add_to_role_policy(iam.PolicyStatement(
            actions=["ssm:PutParameter", "cloudwatch:PutMetricData"],
            resources=["*"]
        ))