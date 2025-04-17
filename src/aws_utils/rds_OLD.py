import boto3
from os import environ as env


# Loads the RDS variable into memory
def load_rds():
    global RDS, TABLE_NAME
    AWS_KEYWORDS = {
        'aws_access_key_id': env['AWS_ACCESS_KEY_ID'],
        'aws_secret_access_key': env['AWS_SECRET_ACCESS_KEY'],
        'region_name': env['RDS_REGION_NAME']
    }
    RDS = boto3.client('rds-data', **AWS_KEYWORDS)
    TABLE_NAME = env['RDS_TABLE_NAME']


# Initial steps to setting up the RDS database
def initialize_rds():
    load_rds() # Ensure RDS and TABLE_NAME are loaded
    execute_sql(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(255),
        directory VARCHAR(50),
        version VARCHAR(50),
        description TEXT
    );
    """)


# Executes SQL coding on the RDS database
def execute_sql(sql):
    return RDS.execute_statement(
        resourceArn=env['RDS_RESOURCE_ARN'],
        secretArn=env['RDS_SECRET_ARN'],
        # database=env['RDS_DATABASE_NAME'],
        sql=sql
    )
    

# Saves metadata to an RDS database
def write_rds(**metadata):
    columns = ', '.join(map(str, metadata.keys()))
    values = ', '.join(map(str, metadata.values()))
    execute_sql(f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values})')
