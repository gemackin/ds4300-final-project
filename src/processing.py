import io, numpy as np
from PIL import Image


# Preprocesses raw data (in bytes form) for storage
def preprocess(data):
    data = np.array(Image.open(io.BytesIO(data)))


# Processes preprocessed data for storage
# This probably being hosted on a lambda?
def process(data):
    # Assuming bytes data (remove this line if already array)
    data = np.array(Image.open(io.BytesIO(data)))
    for i, color in enumerate(('red', 'green', 'blue')):
        yield np.dstack([data[..., i]] * 3)
