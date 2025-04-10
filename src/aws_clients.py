import os, boto3


# Represents the AWS clients (S3 and RDS)
# Is a dictionary because Python importing is weird
AWS_CLIENTS = {}


# Loads the AWS client for S3 and RDS
def load_aws_clients():
    global AWS
    AWS_KEYWORDS = {
        'aws_access_key_id': os.env['AWS_ACCESS_KEY_ID'],
        'aws_secret_access_key': os.env['AWS_SECRET_ACCESS_KEY_ID'],
        'region_name': os.env['REGION_NAME']
    }
    AWS_CLIENTS['S3'] = boto3.client('s3', **AWS_KEYWORDS)
    AWS_CLIENTS['RDS'] = boto3.client('rds', **AWS_KEYWORDS)