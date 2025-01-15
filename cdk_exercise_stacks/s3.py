from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
)
from constructs import Construct
from config import constants

class S3Stack(Stack):
    """
    AWS CDK Stack to create an S3 bucket with event notifications.

    This stack creates an S3 bucket with server-side encryption and sets up an event notification
    to trigger a Lambda function whenever a new object is created in the bucket.
    Methods:
    __init__(scope: Construct, id: str, lambda_stack, **kwargs): Initializes the S3Stack.
    """
    def __init__(self, scope: Construct, id: str, lambda_stack, **kwargs) -> None:
        """
        Initializes the S3Stack.

        Parameters:
        scope (Construct): The scope in which this stack is defined.
        id (str): The unique identifier for this stack.
        lambda_stack (LambdaStack): The Lambda stack containing the Lambda function to be triggered.
        kwargs (dict): Additional keyword arguments for stack configuration.
        """
        
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, "MyBucket",
            bucket_name=constants.S3_BUCKET_NAME,
            encryption=s3.BucketEncryption.S3_MANAGED
        )

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(lambda_stack.lambda_function)
        )