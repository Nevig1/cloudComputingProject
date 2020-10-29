import logging
import boto3
import time

import botocore
from botocore.exceptions import ClientError
from setup import BUCKET_NAME_SETUP

s3 = boto3.resource('s3', region_name="us-east-1")
sqs = boto3.resource("sqs", region_name="us-east-1")


# Function that uploads a file to an s3 bucket
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3', region_name="us-east-1")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# Function that downloads a file from an s3 bucket
def download_file(file_name, bucket_name):
    try:
        s3.Bucket(bucket_name).download_file(file_name, 'new_image.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


if __name__ == "__main__":
    # Instances = ec2.instances.filter()
    KEY = "Docker-Logo2.jpg"
    BUCKET_NAME = "lab1corentintse"
    # Get queues
    inboxQueue = sqs.get_queue_by_name(QueueName='inboxQueue')
    outboxQueue = sqs.get_queue_by_name(QueueName='outboxQueue')
    # Upload an image on S3 bucket
    upload_file(KEY, BUCKET_NAME)
    # Send picture name to EC2 to make image processing
    inboxQueue.send_message(MessageBody=KEY)
    print("key is sent ...")
    while (1):
        print("waiting ...")
        # Get message from EC2 that give the new picture name
        for message in outboxQueue.receive_messages():
            print("Answer: {0}".format(message.body))
            # Download the new picture
            download_file(message.body, BUCKET_NAME)
            message.delete()
            exit(0)

        time.sleep(5)
