from aws_utils import *
from processing import *
from ui import *
from dotenv import load_dotenv


# Loads, processes, and uploads input data
def upload_data(data_raw, metadata, process=True):
    data_preproc = preprocess(data_raw)
    write_aws(data_preproc, directory='preprocessed', **metadata)
    # Processing takes places in a Lambda so we can cut out here
    if not process: return # For debugging, I make it a choice to defer to Lambda
    for data_proc, additional_metadata in process(data_preproc):
        write_aws(data_proc, directory='processed', **metadata, **additional_metadata)


# Full pipeline
def main():
    while True:
        await_button_press()
        data, metadata = read_input()
        print('Processing', metadata['filename'])
        upload_data(data, metadata, process=True)
        populate_analytics()


if __name__ == '__main__':
    load_dotenv()
    initialize_aws_clients()
    initialize_app()
    main()