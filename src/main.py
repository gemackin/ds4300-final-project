from aws_utils import *
from processing import *
from ui import *
from dotenv import load_dotenv


# Loads, processes, and uploads input data
def upload_data(data_raw, metadata):
    data_preproc = preprocess(data_raw)
    write_aws(data_preproc, is_processed=False, **metadata)
    # The following two lines are probably going to be a lambda?
    for data_proc, additional_metadata in process(data_preproc):
        write_aws(data_proc, is_processed=True, **metadata, **additional_metadata)


# Full pipeline
def main():
    for data, metadata in read_input():
        print('Processing', metadata['filename'])
        upload_data(data, metadata)


if __name__ == '__main__':
    load_dotenv()
    prepare_aws_clients()
    initialize_app()
    main()
