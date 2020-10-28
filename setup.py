import boto3
from botocore.exceptions import ClientError

# Create the sqs client using boto3
sqs = boto3.resource("sqs")
# Create the s3 client using boto3
s3 = boto3.client("s3")

try:
    # Create the resquestQueue
    sqs.create_queue(QueueName='requestQueue')
    # Create the responseQueue
    sqs.create_queue(QueueName='responseQueue')
    # s3.create_bucket(Bucket="lab3RequestLogs")
except ClientError as e:
    print(e)
