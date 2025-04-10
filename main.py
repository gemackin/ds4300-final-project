from .src import *
from dotenv import load_dotenv


# Loads, processes, and uploads input data
def upload_data():
    data_raw, metadata = load_input()
    data_preproc = preprocess(data_raw)
    save_aws(data_preproc, is_processed=False, **metadata)
    data_proc = process(data_preproc)
    save_aws(data_proc, is_processed=True, **metadata)



# Full pipeline
def main():
    pass


if __name__ == '__main__':
    load_dotenv()
    main()