import os
from aws_clients import AWS_CLIENTS


# Pipeline for saving a file to AWS (S3 & RDS)
def save_aws(data, filename, **metadata):
    disk_path = save_disk(data, os.path.basename(filename))
    save_s3(disk_path, filename)
    os.remove(disk_path)
    metadata.update(dict(filename=filename))
    save_rds(metadata)


# Saves data to disk as a given filename
def save_disk(data, filename):
    pass


# Saves preprocessed data to an S3 bucket
def save_s3(file_path):
    bucket = os.env['S3_BUCKET_NAME']
    output_path = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        AWS_CLIENTS['S3'].upload_fileobj(file, bucket, output_path)


# Saves metadata to an RDS database
def save_rds(metadata):
    table = os.env['RDS_TABLE_NAME']
    columns = ', '.join(map(str, metadata.keys()))
    values = ', '.join(map(str, metadata.values()))
    sql = 'INSERT INTO {table} ({columns}) VALUES ({values})'
    # TODO: 
    pass