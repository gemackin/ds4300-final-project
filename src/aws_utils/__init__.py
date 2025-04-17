from .rds import *
from .s3 import *
from PIL import Image


# Directory to store uploaded images
UPLOAD_DIR = '../uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Loading and initializing S3 and RDS
def initialize_aws_clients():
    initialize_s3()
    initialize_rds(create_db=False)


# Pipeline for saving a file to AWS (S3 & RDS)
def write_aws(data, filename, directory=None, version=None, **metadata):
    if version is None: version = directory
    else: directory = os.path.join(directory, version).replace('\\', '/')
    disk_path = os.path.join(UPLOAD_DIR, os.path.basename(filename)).replace('\\', '/')
    print(f'Saving {filename} to disk...')
    write_disk(data, disk_path)
    print(f'Saving {filename} to S3...')
    write_s3(disk_path, directory=directory, delete_original=True)
    print(f'Writing {filename} to RDS...')
    write_rds(filename=filename, directory=directory, version=version, **metadata)


# Saves data to disk as a given filename
# Input is NumPy array representing an image
def write_disk(data, filename):
    Image.fromarray(data).save(filename)
    # with open(filename, 'wb') as file:
    #     file.write(data)