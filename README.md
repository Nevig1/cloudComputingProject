# Cloud Computing Project

## Description
This is an AWS application written in python in which a client can submit a request to a worker on an EC2 instance.
Two requests can be send to the EC2 worker.
One containing a list of integers and the other containing an image.

The output of the application is a processed response from the EC2 worker based on the request sent from the client.

## Installation
Use the package manager pip3 to install boto3.
```bash
pip3 install boto3
```

Use the package manager pip3 to install scikit-image.
``` bash
pip3 install scikit-image
```

Create a key pair in the AWS console.
Create an EC2 instance in the AWS console and include your key pair to the instance security.
Create an S3 Bucket in the AWS console and replace BUCKET_NAME_SETUP in setup.py by the name of your S3 Bucket.

Use filezilla to connect to your EC2 instance and upload workerArrayProcessing.py and workerImageProcessing.py to your EC2 instance.
Install boto3 and scikit-image within the EC2 instance python environment using install packaging.

Run the two python files
``` bash
python3 workerArrayProcessing.py&
python3 workerImageProcessing.py&
```

Run the client file in your local environment
``` bash
python3 clientArrayRequest.py&
python3 clientImageRequest.py&
```

## Expected output
List of integers -> Min, Max, Mean, Median of the array (A log file is created on an s3 bucket).

Image -> Upload to an s3 bucket a process of the image sent.

## Authors
Kenza YAHIAOUI
Corentin FERLAY
Given TEFAATAU