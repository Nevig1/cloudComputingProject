import boto3
from botocore.exceptions import ClientError

# Create the sqs client using boto3
sqs = boto3.resource("sqs")
# Create the s3 client using boto3
s3 = boto3.client("s3")
# Bucket Name
BUCKET_NAME_SETUP = 'lab1corentintse'

try:
    # Create the requestQueue
    sqs.create_queue(QueueName='requestQueue')
    # Create the responseQueue
    sqs.create_queue(QueueName='responseQueue')
    # Create the inboxQueue
    sqs.create_queue(QueueName='inboxQueue')
    # Create the outboxQueue
    sqs.create_queue(QueueName='outboxQueue')
except ClientError as e:
    print(e)
