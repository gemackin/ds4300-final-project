from aws_utils import *
from processing import *
from ui import *
from dotenv import load_dotenv


# Loads, processes, and uploads input data
def upload_data(data_raw, metadata, process=True):
    data_preproc = preprocess(data_raw)
    write_aws(data_preproc, is_processed=False, **metadata)
    # Processing takes places in a Lambda so we can cut out here
    if not process: return
    for data_proc, additional_metadata in process(data_preproc):
        write_aws(data_proc, is_processed=True, **metadata, **additional_metadata)


# Full pipeline
def main():
    for data, metadata in read_input():
        print('Processing', metadata['filename'])
        upload_data(data, metadata, process=True)


if __name__ == '__main__':
    load_dotenv()
    initialize_aws_clients()
    initialize_app()
    main()
