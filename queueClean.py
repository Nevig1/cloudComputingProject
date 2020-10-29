import boto3

# Create the sqs client using boto3
sqs = boto3.client("sqs", region_name="us-east-1")

# Create requestQueue with url from queue created
requestQueue = sqs.get_queue_url(QueueName='requestQueue')
# Create responseQueue with url from queue created
responseQueue = sqs.get_queue_url(QueueName='responseQueue')
# Create inboxQueue with url from queue created
inboxQueue = sqs.get_queue_url(QueueName='inboxQueue')["QueueUrl"]
# Create outboxQueue with url from queue created
outboxQueue = sqs.get_queue_url(QueueName='outboxQueue')["QueueUrl"]

# Delete all messages in requestQueue
sqs.purge_queue(QueueUrl=requestQueue["QueueUrl"])
# Delete all messages in responseQueue
sqs.purge_queue(QueueUrl=responseQueue["QueueUrl"])
# Delete all messages in inboxQueue
sqs.purge_queue(QueueUrl=inboxQueue["QueueUrl"])
# Delete all messages in outboxQueue
sqs.purge_queue(QueueUrl=outboxQueue["QueueUrl"])
