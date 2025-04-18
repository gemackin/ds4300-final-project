from aws_utils import *
from processing import *
from ui import *
from dotenv import load_dotenv


# Loads, processes, and uploads input data
def upload_data(data_raw, metadata, do_processing=False):
    print('Preprocessing', metadata['filename'], end='...\n')
    data_preproc = preprocess(data_raw)
    write_aws(data_preproc, directory='preprocessed', **metadata)
    # Processing takes places in a Lambda so we can cut out here
    if not do_processing: return # For debugging, I make it a choice to defer to Lambda
    # print('Processing', metadata['filename'], end='...\n')
    for data_proc, additional_metadata in process(data_preproc, as_bytes=False):
        write_aws(data_proc, directory='processed', **metadata, **additional_metadata)


# Handles form submission and updating analytics
def update_app():
    if get_submit_button():
        data, metadata = read_input()
        upload_data(data, metadata, do_processing=True)
    print('Populating analytics...')
    populate_analytics() # Updating analytics


if __name__ == '__main__':
    print('----- BEGIN SCRIPT -----')
    load_dotenv()
    initialize_aws_clients()
    initialize_app()
    update_app()
    close_rds() # Committing changes to RDS
    print('----- END SCRIPT -----')