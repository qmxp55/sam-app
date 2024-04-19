import json
import boto3
from PIL import Image
from io import BytesIO

def lambda_handler(event, context):
    """Lambda function to generate thumbnail image from S3 and upload to another S3 bucket

    Parameters
    ----------
    event: dict, required
        S3 Event

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    dict
        Lambda response
    """
    
    # Get the S3 client
    s3 = boto3.client('s3')

    # Get the S3 bucket and key from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Get the S3 path
    s3_path = f"s3://{s3_bucket}/{s3_key}"
    print('----> s3_path:', s3_path)
    
    try:
        # Get the object from S3
        response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
        # Read the image data
        image_data = response['Body'].read()
        # Generate thumbnail
        thumbnail_size = (100, 100)  # Define the size of the thumbnail
        image = Image.open(BytesIO(image_data))
        image.thumbnail(thumbnail_size)
        # Save the thumbnail to BytesIO object
        thumbnail_data = BytesIO()
        image.save(thumbnail_data, format=image.format)
        thumbnail_data.seek(0)
        # Upload the thumbnail to s3://{s3_bucket}/outputs/
        dest_bucket = s3_bucket
        dest_key = f"outputs/thumbnail_{s3_key.split('/')[-1]}"
        s3.put_object(Bucket=dest_bucket, Key=dest_key, Body=thumbnail_data)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": error_message
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Thumbnail generated and uploaded successfully",
            "s3_path": f"s3://{dest_bucket}/{dest_key}"
        })
    }