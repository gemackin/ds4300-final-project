from .rds import *
from .s3 import *


# Directory to store uploaded images
UPLOAD_DIR = '../uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Loading and initializing S3 and RDS
def initialize_aws_clients():
    initialize_s3()
    initialize_rds()


# Pipeline for saving a file to AWS (S3 & RDS)
def write_aws(data, filename, directory=None, **metadata):
    disk_path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
    write_disk(data, disk_path)
    write_s3(disk_path, directory=directory, delete_original=True)
    write_rds(filename=filename, directory=directory, **metadata)


# Saves data to disk as a given filename
def write_disk(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)