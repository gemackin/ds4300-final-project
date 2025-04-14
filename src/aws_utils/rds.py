import os, boto3


# Loads the RDS variable into memory
def load_rds():
    global RDS, TABLE_NAME
    AWS_KEYWORDS = {
        'aws_access_key_id': os.env['AWS_ACCESS_KEY_ID'],
        'aws_secret_access_key': os.env['AWS_SECRET_ACCESS_KEY_ID'],
        'region_name': os.env['REGION_NAME']
    }
    RDS = boto3.client('rds-data', **AWS_KEYWORDS)
    DATABASE_NAME = os.env['RDS_DATABASE_NAME']
    TABLE_NAME = os.env['RDS_TABLE_NAME']


# Initial steps to setting up the RDS database
def initialize_rds():
    pass


# Saves metadata to an RDS database
def write_rds(metadata):
    columns = ', '.join(map(str, metadata.keys()))
    values = ', '.join(map(str, metadata.values()))
    run_sql(f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values})')
