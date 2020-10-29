import os

import boto3
import time
import math
from datetime import datetime

# Create the sqs client using boto3
from botocore.exceptions import ClientError
from pip.utils import logging
from setup import BUCKET_NAME_SETUP

sqs = boto3.client("sqs")


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


while (1):
    # Create requestQueue with url from queue created
    requestQueue = sqs.get_queue_url(QueueName='requestQueue')["QueueUrl"]
    # Create responseQueue with url from queue created
    responseQueue = sqs.get_queue_url(QueueName='responseQueue')["QueueUrl"]
    print("Retrieving messages...")
    # Get the response from client in requestQueue
    response = sqs.receive_message(QueueUrl=requestQueue)
    if "Messages" in response:
        # Get the right message from the requestQueue
        message = response['Messages'][0]
        print(message)
        print('New message: {0}'.format(message["Body"]))
        # Message parsing
        numbers = message["Body"].split()
        min = 0
        max = 0
        tot = 0
        median = 0
        i = 0
        # Go through all the numbers in the array
        while i < len(numbers):
            # Compute the sum of the numbers in the array
            tot += int(numbers[i])
            # Handle case : array is empty
            if i == 0:
                min = int(numbers[i])
                max = min
                mean = min
                median = min
            # Handle case : array is not empty
            else:
                # Number min of the array
                if int(numbers[i]) < min:
                    min = int(numbers[i])
                # Number max of the array
                if int(numbers[i]) > max:
                    max = int(numbers[i])
            i += 1
        # Compute the mean of the array
        mean = tot / len(numbers)
        # Get the position of the median with index in array
        index = int(math.ceil(len(numbers) / 2) if len(numbers) %
                                                   2 != 0 else len(numbers) / 2 + 1)
        # Sort the numbers in the array
        numbers = sorted(numbers)
        # Compute the median of the array
        median = numbers[index]
        # Format answer with Min, Max, Mean, Median
        answer = 'Min: {0}, Max: {1}, Mean: {2}, Median: {3}'.format(
            min, max, mean, median)
        print(answer)
        # Send the processed answer through responseQueue
        sqs.send_message(
            QueueUrl=responseQueue, MessageBody=answer)
        # Get the unique id of the message in order to delete it from the queue
        receipt_handle = message['ReceiptHandle']
        # Delete the message from the queue with its unique id
        sqs.delete_message(
            QueueUrl=requestQueue, ReceiptHandle=receipt_handle)
        # Get the time
        now = datetime.now()
        # Create the log file
        filename = "log-" + now.strftime("%d_%m_%y-%H_%M") + ".txt"
        # Open the log file
        logfile = open(filename, "w+")
        # Write the inputs ie array in the log file
        logfile.write("Inputs: " + ', '.join(numbers) + '\n')
        # Write the processed output in the log file
        logfile.write("Answer: " + answer)
        # Close the log file
        logfile.close()
        # Define the bucket name for log upload
        BUCKET_NAME = BUCKET_NAME_SETUP
        # Upload the log file to s3 Bucket
        upload_file(filename,BUCKET_NAME)
        # Remove the log file from local
        os.remove(logfile)
    time.sleep(1)
