import os, boto3
from os import environ as env


# Loading the S3 variables into memory
def load_s3():
    global S3, BUCKET_NAME
    AWS_KEYWORDS = {
        'aws_access_key_id': env['AWS_ACCESS_KEY_ID'],
        'aws_secret_access_key': env['AWS_SECRET_ACCESS_KEY'],
        'region_name': env['AWS_REGION_NAME']
    }
    S3 = boto3.client('s3', **AWS_KEYWORDS)
    BUCKET_NAME = env['S3_BUCKET_NAME']


# Initial steps to setting up the S3 bucket
def initialize_s3():
    load_s3()


# Loads data from an S3 bucket
def read_s3(*filename):
    filename = os.path.join(*filename)
    data = S3.get_object(Bucket=BUCKET_NAME, Key=filename)
    return data['Body'].read()


# Saves preprocessed data to an S3 bucket
def write_s3(disk_path, directory=None, delete_original=True):
    s3_path = os.path.basename(disk_path)
    if directory: # Adding a folder to path
        s3_path = os.path.join(directory, s3_path)
    with open(disk_path, 'rb') as file:
        S3.upload_fileobj(file, BUCKET_NAME, s3_path)
    if delete_original:
        os.remove(disk_path)