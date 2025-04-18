from urllib import parse
import os, io, cv2
import aws_utils as aws, numpy as np
from dotenv import load_dotenv


# Converting bytes data of an image to a NumPy array
# Used since PIL installation doesn't work on Lambda
def read_bytes(data, filename='temp.png'):
    with open(filename, 'wb') as file:
        file.write(data)
    data = cv2.imread(filename)
    return cv2.cvtColor(data, cv2.COLOR_BGR2RGB)


# Processes preprocessed data for storage
def process(data, as_bytes=True):
    # Assuming bytes data (remove this line if already array)
    if as_bytes:
        data = np.array(read_bytes(data))
    for i, color in enumerate(('red', 'green', 'blue')):
        metadata =  {'version': f'{color}_grayscale'}
        yield np.dstack([data[..., i]] * 3), metadata


def lambda_handler(event, context):
    load_dotenv()
    aws.initialize_aws_clients()

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    filename = parse.unquote_plus(key, encoding='utf-8')

    if bucket != os.environ['S3_BUCKET_NAME']: return
    if not filename.startswith('preprocessed'): return

    data_preproc = aws.read_s3(filename)
    filename_out = os.path.basename(filename)
    for data_proc, metadata in process(data_preproc, as_bytes=True):
        aws.write_aws(data_proc, directory='processed', filename=filename_out, **metadata)
    aws.close_rds()
