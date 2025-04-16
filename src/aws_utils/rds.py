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
    load_rds() # Ensure RDS and TABLE_NAME are loaded
    execute_sql(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(255),
        version VARCHAR(50),
        description TEXT
    );
    """)


def execute_sql(sql):
    return RDS.execute_sql(sql)
    # response = RDS.execute_statement(
    #     resourceArn=os.environ['RDS_RESOURCE_ARN'],
    #     secretArn=os.environ['RDS_SECRET_ARN'],
    #     database=os.environ['RDS_DATABASE_NAME'],
    #     sql=create_table_sql
    # )
    

# Saves metadata to an RDS database
def write_rds(metadata):
    columns = ', '.join(map(str, metadata.keys()))
    values = ', '.join(map(str, metadata.values()))
    execute_sql(f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values})')
