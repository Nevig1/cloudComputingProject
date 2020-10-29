import boto3
import botocore
import time
import os
from botocore.exceptions import ClientError
from pip.utils import logging
from skimage import io
from skimage.color import rgb2hsv
from setup import BUCKET_NAME_SETUP


# Function that uploads a file to an s3 bucket
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# Function that downloads a file from an s3 bucket
def download_file(file_name, bucket_name):
    try:
        s3.Bucket(bucket_name).download_file(file_name, 'my_local_image.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


BUCKET_NAME = BUCKET_NAME_SETUP
sqs = boto3.client("sqs")
s3 = boto3.resource('s3')
# Create inboxQueue with url from queue created
inboxQueue = sqs.get_queue_url(QueueName='inboxQueue')["QueueUrl"]
# Create outboxQueue with url from queue created
outboxQueue = sqs.get_queue_url(QueueName='outboxQueue')["QueueUrl"]
while (1):
    print("Retrieving messages...")
    response = sqs.receive_message(QueueUrl=inboxQueue)
    # Get message
    if "Messages" in response:
        message = response['Messages'][0]
        # Get image name
        KEY = message["Body"]
        # Download image on S3 bucket
        download_file(KEY, BUCKET_NAME)
        # Image processing
        img = io.imread(KEY)
        processed_img = rgb2hsv(img)
        io.imsave("new_image.jpg", processed_img)
        # Upload new image to S3 bucket
        upload_file("new_image.jpg", BUCKET_NAME)
        # Remove files
        os.remove(KEY)
        os.remove("new_image.jpg")
        # Send new message to the client
        sqs.send_message(
            QueueUrl=outboxQueue, MessageBody="new_image.jpg")
        # Delete the message with unique id
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=inboxQueue, ReceiptHandle=receipt_handle)
    time.sleep(5)
