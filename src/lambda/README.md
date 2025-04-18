# AWS Lambda Instance

All of the code in this folder will not be used by EC2, but rather by Lambda.

Lambda has been set up to respond to any file created in the `preprocessed/` folder within S3.
The handler will initiate the processing step, which will then save three additional versions of the file,
a grayscale for each color component (red, green, and blue).
These files will be saved into the `processed/` folder within S3.

## How to set up Lambda

1. Install `pymysql`, `opencv-python`, and `numpy` in this directory
    - Run `pip install <library> -t . --no-user` in your local terminal
    - Since the Lambda doesn't appear to have any libraries pre-installed
2. Compress the contents of this directory into a `.zip` file
3. Upload the `.zip` file from step 1 into the Lambda
4. Upload your configured `src/.env` file into the Lambda
5. Set up a rule for the Lambda to trigger whenever a file is created in the S3 bucket