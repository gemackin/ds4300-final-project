import io, numpy as np
from PIL import Image


SHAPE = (100, 100)


# Preprocesses raw data (in bytes form) for storage
def preprocess(data):
    data = Image.open(io.BytesIO(data))
    return np.array(data.resize(SHAPE))


# Processes preprocessed data for storage
def process(data, as_bytes=True):
    # Assuming bytes data (remove this line if already array)
    if as_bytes:
        data = np.array(Image.open(io.BytesIO(data)))
    for i, color in enumerate(('red', 'green', 'blue')):
        metadata =  {'version': f'{color}_grayscale'}
        yield np.dstack([data[..., i]] * 3), metadata