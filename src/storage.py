import os


# Pipeline for saving a file to AWS (S3 & RDS)
def save_aws(data, filename, **metadata):
    file_path = save_disk(data, os.path.basename(filename))
    save_s3(file_path, filename)
    metadata.update(dict(filename=filename))
    save_rds(metadata)


# Saves data to disk as a given filename
def save_disk(data, filename):
    pass


# Saves preprocessed data to an S3 bucket
def save_s3(file_path):
    pass


# Saves metadata to an RDS database
def save_rds(metadata):
    pass