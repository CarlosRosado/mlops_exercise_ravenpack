import boto3
import os
from config import constants

def lambda_handler(event, context):
    """
    AWS Lambda function to update an SSM parameter with the key of a newly created S3 object.
    This function is triggered by S3 events. When a new object is created in an S3 bucket.

    Parameters:
    event (dict): The event data that triggered the function. This includes details about the S3 event.
    context (object): The context in which the function is called. Provides runtime information.

    Returns:
    dict: A response object containing the status code and a message indicating the SSM parameter update status.
    """
    ssm_client = boto3.client('ssm')
    s3_event = event['Records'][0]['s3']
    bucket_name = s3_event['bucket']['name']
    object_key = s3_event['object']['key']
    
    ssm_parameter_name = constants.SSM_PARAMETER_MODEL
    ssm_client.put_parameter(
        Name=ssm_parameter_name,
        Value=f"s3://{bucket_name}/{object_key}",
        Type='String',
        Overwrite=True
    )
    return {
        'statusCode': 200,
        'body': f"SSM parameter {ssm_parameter_name} updated with {object_key}"
    }