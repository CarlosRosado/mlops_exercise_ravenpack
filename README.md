# Welcome to your CDK-Exercise Python project!

In this exercise, you will simulate the completion of a usual sprint task.

You will need to use AWS Cloud Development Kit (https://aws.amazon.com/cdk/).
Here you have some steps about how to install it:

## Installing AWS CDK CLI

Install the AWS CDK CLI globally using the following Node Package Manager command.

```commandline
npm install -g aws-cdk
```

> If you get a permission error, and have administrator access on your system, try `sudo npm install -g aws-cdk`.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

If during the development of the exercise, you need to add additional dependencies, 
for example other CDK libraries, just add them to the requirements.txt.

## Useful CDK commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation

## Testing

At this point you can also run the tests either by integrating the exercise code in an IDE (Visual Studio Code, PyCharm,
etc.) or by running this command from the root of the project:

```commandline
$ pytest tests
```

Time to really start:

# MLOps Engineer - Exercise

The product team has asked us to prepare a quick pipeline for being able to test ML models delivered by the Data Science team. 
This pipeline will be used during the prototyping/testing phase, so we need to be able to deploy it quickly and easily.

The agreement with the Data Science team is that they will deliver a model on an AWS S3 bucket, and we will have to deploy it as a SageMaker endpoint.

The suggested pipeline will have the following steps:
- The model is delivered to an S3 bucket.
- A Lambda function is triggered by the S3 event and will register the model key in SSM.
- A new sagemaker endpoint is created with the model registered in SSM.

In RavenPack, we appreciate our Infrastructure-as-Code divided into several stacks, using the CDK framework.

An important part of the exercise is to document very well the decisions and arguments you may have made during the development of the task.

The exercise does not require previous experience with CDK or sagemaker, since all the information needed can be found on the documentation. 

The exercise includes a few unit tests that can be used to validate the solution and to know specific details about the expected behavior. They can be changed/adapted if a different approach is taken, but ensure that this is correctly documented.

The proposed solution is divided into 3 different stacks and the implementation code for the lambda function:

## S3 stack

- Add an S3 bucket where the models will be placed
- The bucket needs to have versioning enabled and AES256 Server-Side Encryption.
- It needs to create the S3 event that will trigger the lambda function
 

## Lambda stack

- A lambda is created that has permission to write to SSM. In the future, we might want to put metrics to cloudwatch. Therefore, this permission is also required.
- The lambda will read the SSM key from an environment variable. This key will be used to store the S3 Object key of the model received.
- The implementation code of the lambda function is required.


## Sagemaker stack

- A sagemaker endpoint is created with the model that is registered in SSM.
- The model uses torch and transformers libraries. A sagemaker model image that supports these libraries is required.
- The endpoint needs to have an autoscaling rule based on the CPU utilization.

## Constants file

There is a `config/constants.py` file that contains many of the configuration parameters you will need to integrate into
the CDK code. Please give this file a look before jumping directly to the exercise.

## Testing

There is a `tests/unit/` folder with unit tests. They can be changed/adapted due to the different approaches taken, but ensure that this is correctly documented.

## Exercise completion

Please add your code to the skeleton stacks defined in each of the files found in the `cdk_exercise_stacks` folder,
respecting the definition found in the `app.py` file.

After the completion, please create a zip file with the project. Please do not forget the documentation.

In addition to the implementation, please provide a brief explanation about these questions:

- How would you implement an automated model monitoring system once the endpoint is live?
- In addition to the compressed model, imagine that you also receive the model's training metrics. How would you properly register the model with these metrics so that future models can be automatically compared with the previous ones?