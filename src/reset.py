from aws_utils import *
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    initialize_rds(True)