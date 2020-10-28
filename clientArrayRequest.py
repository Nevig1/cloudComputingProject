import boto3
import time

sqs = boto3.client("sqs")

if __name__ == "__main__":
    # Create requestQueue with url from queue created
    requestQueue = sqs.get_queue_url(QueueName='requestQueue')["QueueUrl"]
    # Create responseQueue with url from queue created
    responseQueue = sqs.get_queue_url(QueueName='responseQueue')["QueueUrl"]
    # Send an array of numbers through requestQueue
    sqs.send_message(
        QueueUrl=requestQueue, MessageBody='1 2 2 1 6 74 0 2 4 2 2 14 2 22 8 2 10 3 2 1')
    while True:
        # Get the number of messages in the responseQueue
        numberOfMessagesInQueue = sqs.get_queue_attributes(QueueUrl=responseQueue,
                                                           AttributeNames=['ApproximateNumberOfMessages'])
        # Check if the number of messages in the responseQueue is not empty
        if numberOfMessagesInQueue['Attributes']['ApproximateNumberOfMessages'] == '0':
            print("Checking answer...")
            time.sleep(1)
        else:
            break
    # Get the response from ec2 instance in responseQueue
    response = sqs.receive_message(QueueUrl=responseQueue)
    if "Messages" in response:
        # Get the right message in the response from ec2 instance
        message = response["Messages"][0]
        print(message['Body'])
        # Get the unique id of the message in order to delete it from the queue
        receipt_handle = message['ReceiptHandle']
        # Delete the message from the queue with its unique id
        sqs.delete_message(QueueUrl=responseQueue, ReceiptHandle=receipt_handle)
