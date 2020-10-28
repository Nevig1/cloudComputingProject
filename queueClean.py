import boto3

# Create the sqs client using boto3
client = boto3.client("sqs")

# Create requestQueue with url from queue created
requestQueue = client.get_queue_url(QueueName='requestQueue')
# Create responseQueue with url from queue created
responseQueue = client.get_queue_url(QueueName='responseQueue')

# Delete all messages in requestQueue
client.purge_queue(QueueUrl=requestQueue["QueueUrl"])
# Delete all messages in responseQueue
client.purge_queue(QueueUrl=responseQueue["QueueUrl"])
