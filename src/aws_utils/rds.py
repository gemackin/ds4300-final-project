import pymysql, re
from os import environ as env


# Creates a new database for the RDS instance
# We delete the previous instance 
def create_database(delete_previous=False):
    connection = pymysql.connect(
        host=env['RDS_ENDPOINT_URL'],
        user=env['RDS_USERNAME'],
        password=env['RDS_PASSWORD'],
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    if delete_previous:
        cursor.execute(f'DROP DATABASE IF EXISTS `{env["RDS_DATABASE_NAME"]}`')
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{env["RDS_DATABASE_NAME"]}`')
    cursor.close()
    connection.close()


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
def initialize_rds(create_db=False):
    if create_db:
        print('Creating database')
        create_database(delete_previous=True)
    # print('Loading RDS variables')
    load_rds() # Ensure RDS and TABLE_NAME are loaded
    if not create_db: return
    print('Creating table')
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
    sanitize = lambda x: x.replace('"', '') # I'm just removing quotes
    add_quotes = lambda x: f'"{sanitize(x)}"' if isinstance(x, str) else x
    values = ', '.join(map(str, list(map(add_quotes, metadata.values()))))
    execute_sql(f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values})')


def close_rds():
    CONNECTION.commit()
    CONNECTION.close()