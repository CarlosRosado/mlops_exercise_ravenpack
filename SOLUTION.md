# SOLUTION

This document explains how the questions in README.md were resolved to complete the challenge.

## 1. Install AWS CDK and Python Dependencies

First, install the AWS CDK globally using npm. This allows you to use the CDK CLI to manage our AWS infrastructure as code.

Next, install the required Python dependencies listed in requirements.txt and inside requirements-dev.txt. This ensures that all necessary libraries are available for our project.

## 2. Bootstrap the CDK Environment

Bootstrap the CDK environment to prepare it for deploying AWS resources. This step sets up the necessary resources in our AWS account to support the CDK.

## 3. Define Constants

To correctly perform this exercise, We only need to modify the `SAGEMAKER_MODEL_IMAGE` variable. This constant is used to specify the Docker image for the SageMaker model, which is essential because it contains the environment and dependencies needed to run the model inference.

For this exercise, I’ve selected the Docker image `763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-inference:1.5.1-cpu-py36-ubuntu16.04` for several important reasons:

1. **Compatibility**: This image is designed to work seamlessly with the PyTorch framework, which is a popular choice for machine learning and deep learning applications. This ensures that the model will be deployed and run successfully on SageMaker.

2. **Pre-built and Optimized**: The image comes pre-built and optimized specifically for inference tasks. It already includes all the necessary libraries and dependencies required to execute the model, which simplifies the setup process and saves time compared to setting up everything from scratch.

3. **CPU-based**: This particular image is optimized for CPU-based instances, which are more cost-effective while still being adequate for many inference tasks. Since the goal of this exercise is to focus on the deployment process rather than high-performance optimization, this choice is ideal.

4. **AWS Support**: The image is provided and maintained by AWS. This means it is regularly updated, supported, and includes the latest security patches and improvements. This reduces the risk of any compatibility issues and ensures that the environment remains secure and up-to-date.

By setting `SAGEMAKER_MODEL_IMAGE` to this specific image, I can ensure that the deployment process will be smooth and that the model runs in a well-supported and optimized environment.

## 4. Implement the Lambda Function

I updated the file lambda_handler.py to encapsulate the code within a Lambda function.

This file now contains the code for an AWS Lambda function that gets triggered by S3 events. Whenever a new object is added to an S3 bucket, the function runs automatically. Its main purpose is to update an SSM (AWS Systems Manager) parameter with the key of the newly created S3 object.

The entry point for the function is lambda_handler, which AWS Lambda invokes when the function is triggered. It takes two parameters: event, which provides details about the triggering event (in this case, an S3 event), and context, which contains information about the function's runtime and invocation.

Within the function, I created an SSM client using the boto3 library. The function extracts the bucket name and the key (path) of the newly added S3 object from the event dictionary.

The name of the SSM parameter is retrieved from an environment variable. This makes the function more flexible and easier to manage since the parameter name can be configured outside the code. If needed, this environment variable could also be defined in a constants file.

Using the SSM client, the function updates the parameter with the new S3 object key. It sets the parameter name, assigns its value (the S3 URI of the object), defines the type as a string, and ensures it overwrites any existing parameter with the same name.

Finally, the function returns a response confirming the successful update of the SSM parameter. The response includes a 200 HTTP status code and a message indicating which SSM parameter was updated and its new value.


## 5. Update the S3 Stack

The s3.py file is where I defined an AWS S3 stack using AWS CDK. This stack is responsible for creating an S3 bucket with specific configurations and setting up an event notification to trigger a Lambda function whenever a new object is added to the bucket.

I created the S3Stack class by extending the Stack class. The constructor for this class accepts the following parameters:

* **scope:** Indicates the scope where the stack is defined.
* **id:** A unique identifier for the stack.
* **lambda_stack:** Passes the Lambda stack so I can configure the event notification.
Within the constructor, I used the super() function to initialize the base Stack class with the given scope and id.

The S3 bucket is created using the s3.Bucket class, and I configured it with the following properties:

* **bucket_name:** Sets the name of the bucket.
* **encryption:** Enables server-side encryption with S3-managed keys (SSE-S3) to enhance security.
* **versioned:** Activates versioning to allow multiple versions of objects to be stored in the bucket.

After the bucket is created, I added an event notification using the add_event_notification method. This notification triggers the Lambda function whenever a new object is added to the bucket. I specified the event type as s3.EventType.OBJECT_CREATED and used the s3_notifications.LambdaDestination class to set the Lambda function as the destination for the event.


## 6. Update the Lambda Stack

In the lambda_functions.py file, I defined an AWS Lambda stack using AWS CDK. This stack sets up a Lambda function with specific configurations and attaches the required IAM policies, enabling the function to interact with other AWS services.

I created the LambdaStack class by extending the Stack class. The constructor of this class takes the following parameters:

* **scope:** Defines the scope where the stack is created.
* **id:** A unique identifier for the stack.
* **kwargs:** Additional configuration options for the stack.

Within the constructor, I used the Environment class to specify the AWS account and region. I then called the super() function to initialize the base Stack class with the provided scope, id, and environment configuration.

The Lambda function is defined using the aws_lambda.Function class, and I configured it with the following properties:

* **runtime:** Sets the runtime environment for the Lambda function (e.g., Python 3.10).
* **handler:** Specifies the function's handler method.
* **code:** Defines the location of the Lambda function code.
* **function_name:** Sets the name of the Lambda function.
* **environment:** Configures environment variables for the Lambda function.
* **timeout:** Specifies the maximum execution time for the Lambda function.

After creating the Lambda function, I attached the necessary IAM policies to its execution role. I included the AWSLambdaBasicExecutionRole managed policy to grant basic execution permissions and the AmazonSSMFullAccess managed policy to enable interaction with the SSM service.


## 7. Update the SageMaker Endpoint Stack

In the sagemaker_endpoints.py file, I defined an AWS SageMaker endpoint stack using AWS CDK. This stack sets up a SageMaker model, an endpoint configuration, and an endpoint, along with an autoscaling policy to scale the endpoint based on usage.

I created the SentimentEndpointStack class by extending the Stack class. The constructor takes several parameters:

* **scope:** Specifies the scope where this stack is defined.
* **id:** A unique identifier for the stack.
* **kwargs:**  Allows for additional configuration options.

Inside the constructor, I used the super() function to initialize the base Stack class with the provided scope and id.

### SageMaker Model

I created a SageMaker model using the aws_sagemaker.CfnModel class and configured it with:

* **model_name:** Defines the name of the model.
* **primary_container:** Specifies the container details, such as the Docker image and model data URL.

### Endpoint Configuration

Next, I defined the endpoint configuration using the aws_sagemaker.CfnEndpointConfig class. The configuration includes:

* **production_variants:** Sets up production variants with instance type, initial instance count, model name, and variant name.

### SageMaker Endpoint

I then created a SageMaker endpoint using the aws_sagemaker.CfnEndpoint class, which was configured with:

* **endpoint_config_name:** Specifies the endpoint configuration's name.
* **tags:** Adds tags to help manage and identify the endpoint.

### Autoscaling Configuration

For scaling, I added an autoscaling target using the aws_applicationautoscaling.ScalableTarget class. Its configuration includes:

* **service_namespace:** Specifies SageMaker as the service namespace.
* **max_capacity:** Sets the maximum number of instances.
* **min_capacity:** Sets the minimum number of instances.
* **resource_id:** Identifies the autoscaling target resource.
* **scalable_dimension:** Defines the scalable dimension.

### Autoscaling Policy

To manage scaling behavior, I added an autoscaling policy using the aws_applicationautoscaling.TargetTrackingScalingPolicy class. The policy was configured with:

* **scaling_target:** Associates the policy with the scaling target.
* **target_value:** Defines the desired utilization target.
* **predefined_metric:** Specifies the metric for scaling decisions.
* **scale_in_cooldown:** Sets the cooldown period for scaling in.
* **scale_out_cooldown:** Sets the cooldown period for scaling out.

## 8. Run and Adapt Unit Tests

Unit tests are essential for ensuring that the individual components in my project behave as expected. Here are some examples of the unit tests I’ve written, along with their purposes:

1. S3 Bucket Creation Test

    * This test validates that the S3 bucket is created with the correct properties, such as the bucket name, encryption, and versioning configuration.

    * It checks that server-side encryption is enabled, the bucket name is accurate, and versioning is properly set up.

2. Lambda Function Creation Test

    * This test ensures that the Lambda function is created with the appropriate properties, including the handler, runtime, environment variables, and timeout settings.

    * It verifies that the handler method, runtime environment, environment variables, and timeout are all correctly defined.

3. Lambda Role Creation Test

    * This test confirms that the Lambda function’s execution role is created with the necessary managed policies.

    * It checks that the role includes both the AWSLambdaBasicExecutionRole and AmazonSSMFullAccess policies.

4. SageMaker Endpoint Creation Test

    * This test ensures that the SageMaker endpoint is created with the correct endpoint configuration name and tags.

    * It validates that the endpoint is properly configured with the expected name and tags.

5. SageMaker Endpoint Configuration Test

    * This test verifies that the SageMaker endpoint configuration is correctly set up with the appropriate production variants.

    * It checks the instance type, initial instance count, model name, and variant name for accuracy.

6. SageMaker Model Creation Test

    * This test confirms that the SageMaker model is created with the correct properties, including the model name and primary container details.

    * It validates the model name, Docker image, and model data URL.

7. Autoscaling Policy Creation Test

    * This test ensures that the autoscaling policy is configured with the correct settings, such as the scaling target, target value, predefined metric, and cooldown periods.

    * It checks that the scaling target, target value, predefined metric, scale-in cooldown, and scale-out cooldown are all properly defined.

## Exercise completion

### 1. How would you implement an automated model monitoring system once the endpoint is live?

To implement an automated model monitoring system after the endpoint is live, I would utilize various AWS services and features to ensure the model's performance and reliability are continuously tracked and maintained.

First, I’d enable **Amazon CloudWatch Metrics** to monitor key performance indicators such as invocation counts, latency, and error rates. These metrics are essential for gaining insights into the model's performance and overall health, helping to promptly identify any anomalies or issues.

Next, I would set up **CloudWatch Alarms** to automatically trigger notifications or actions when specific thresholds are exceeded. For instance, alarms can be configured for high error rates or increased latency, which might indicate underlying issues with the model or infrastructure. These alarms can be integrated with **Amazon SNS (Simple Notification Service)** to send automated alerts to the appropriate stakeholders.

In addition, I’d enable logging for model predictions and input data, directing them to **Amazon CloudWatch Logs** or **Amazon S3**. This would allow for ongoing analysis of the model's performance and detection of anomalies or data drift. Implementing custom metrics to track specific aspects of the model’s behavior could provide even more detailed monitoring.

To maintain accuracy and reliability, I’d schedule periodic evaluations of the model using **Amazon SageMaker's built-in capabilities** or custom evaluation scripts. By comparing predictions against ground truth data, I can assess the model’s accuracy and detect performance degradation. If issues are identified, I’d implement an automated pipeline for retraining and deploying the updated model. Tools like **AWS Step Functions** or **Amazon SageMaker Pipelines** would be ideal for orchestrating the retraining process and managing deployment to the endpoint.

### 2. How would you properly register the model with these metrics so that future models can be automatically compared with the previous ones?

To properly register a model with its training metrics and enable automatic comparisons with future models, I would follow these steps:

First, I’d use **Amazon SageMaker Model Registry** to create a centralized repository for managing and tracking machine learning models. The Model Registry provides a structured way to store model versions along with their metadata, including training metrics.

When registering a new model, I’d include the training metrics as part of its metadata. This involves creating a model package that contains both the model artifacts and the associated training metrics. These metrics might include key performance indicators such as accuracy, precision, recall, F1 score, or any other relevant measurements.

To ensure the metrics are easily accessible, I’d store them in a structured format like JSON or CSV and include them in the model package. This approach makes it simple to retrieve and use the metrics for comparison with future models.

Using Amazon SageMaker's built-in capabilities, I’d automate the process of comparing new models to their previous versions. Whenever a new model is registered, SageMaker can compare its training metrics to those of prior models, making it easier to identify improvements or regressions in performance.

Finally, I’d configure automated notifications or actions based on the comparison results. For example, if the new model demonstrates significantly better performance, I could automate its promotion to production. Conversely, if its performance is worse, I’d set up alerts to initiate further investigation. This ensures the model development and deployment process remains efficient and reliable.