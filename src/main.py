from aws_utils import *
from processing import *
import ui # Can't do "from" when uninitialized
import sys
from dotenv import load_dotenv


# Loads, processes, and uploads input data
def upload_data(data_raw, metadata, process=True):
    data_preproc = preprocess(data_raw)
    write_aws(data_preproc, directory='preprocessed', **metadata)
    # Processing takes places in a Lambda so we can cut out here
    if not process: return # For debugging, I make it a choice to defer to Lambda
    for data_proc, additional_metadata in process(data_preproc):
        write_aws(data_proc, directory='processed', **metadata, **additional_metadata)


# Stuck in infinite loop until the user presses a button
def await_button_press():
    while True:
        if ui.EXIT_BUTTON:
            print('Shutting down the application...')
            sys.exit(0) # Quit the program
        if ui.SUBMIT_BUTTON:
            print('Reading input...')
            return 'submit' # Stop waiting to read input
    raise Exception('How in the world did you trigger this?')


# Full pipeline
def main():
    while True:
        await_button_press()
        data, metadata = ui.read_input()
        print('Processing', metadata['filename'])
        upload_data(data, metadata, process=True)
        ui.populate_analytics()


if __name__ == '__main__':
    load_dotenv()
    initialize_aws_clients()
    ui.initialize_app()
    main()