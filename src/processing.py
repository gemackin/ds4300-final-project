import io, numpy as np
from PIL import Image


# Preprocesses raw data (in bytes form) for storage
def preprocess(data):
    data = np.array(Image.open(io.BytesIO(data)))


# Processes preprocessed data for storage
# This probably being hosted on a lambda?
def process(data):
    pass
