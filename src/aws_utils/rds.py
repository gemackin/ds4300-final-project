import pymysql
from os import environ as env


# Loads the RDS variable into memory
def load_rds():
    global CONNECTION, TABLE_NAME
    CONNECTION = pymysql.connect(
        host=env['RDS_ENDPOINT_URL'],
        user=env['RDS_USERNAME'],
        password=env['RDS_PASSWORD'],
        database=env['RDS_DATABASE_NAME'],
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
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
    with CONNECTION.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()
    

# Saves metadata to an RDS database
def write_rds(**metadata):
    columns = ', '.join(map(str, metadata.keys()))
    values = ', '.join(map(str, metadata.values()))
    execute_sql(f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values})')
