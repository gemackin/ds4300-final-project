# AWS Lambda Instance

All of the code in this folder will not be used by EC2, but rather by Lambda.

Lambda has been set up to respond to any file created in the `preprocessed/` folder within S3.
The handler will initiate the processing step, which will then save three additional versions of the file,
a grayscale for each color component (red, green, and blue).
These files will be saved into the `processed/` folder within S3.

## How to set up the Lambda

1. Upload all the code in this folder into the Lambda
2. Upload each file from `src/aws_utils/` into the Lambda as well
3. Rename `__init__.py` from step 2 to `aws_utils.py`
