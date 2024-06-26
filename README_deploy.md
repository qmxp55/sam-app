
This project contains source code and supporting files for a serverless application to generate Thumbnail images that you can deploy with the SAM CLI. It includes the following files and folders.

- thumbnail_generator - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. 

## Deploy the application

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided
```

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Add policy to `ThumbnailGeneratorFunctionRole.Arn` Role to get `s3:GetObject` and `s3:utObject` access

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::storitmp/*"
            ]
        }
    ]
}
```