LAMBDA_HANDLER = "lambda_handler.lambda_handler"
LAMBDA_NAME = "s3-object-to-ssm"
LAMBDA_RUNTIME = "python3.10"
LAMBDA_ENVIRONMENT_VARIABLE = {
    'SSM_SENTIMENT_MODEL': 'sentiment_model/latest_object_key'
}

S3_BUCKET_NAME = "cdk-exercise-bucket"

SAGEMAKER_ENDPOINT_NAME = "sagemaker-endpoint"
SSM_PARAMETER_MODEL = "sentiment-model"
SAGEMAKER_MODEL_IMAGE = "763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-inference:1.5.1-cpu-py36-ubuntu16.04"
SAGEMAKER_INSTANCE_TYPE = "ml.g4dn.xlarge"
SCALEINCOOLDOWN = 300
SCALEOUTCOOLDOWN = 300
TARGET_VALUE = 70