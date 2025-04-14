from .rds import *
from .s3 import *


# Loading and initializing S3 and RDS
def prepare_aws_clients():
    load_s3()
    initialize_s3()
    load_rds()
    initialize_rds()


# Pipeline for saving a file to AWS (S3 & RDS)
def write_aws(data, filename, **metadata):
    disk_path = write_disk(data, os.path.basename(filename))
    write_s3(disk_path, delete_original=True)
    metadata.update(dict(filename=filename))
    write_rds(metadata)


# Saves data to disk as a given filename
def write_disk(data, filename):
    pass