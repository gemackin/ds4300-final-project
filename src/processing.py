import io, numpy as np
from PIL import Image


SHAPE = (100, 100)


# Preprocesses raw data (in bytes form) for storage
def preprocess(data):
    data = Image.open(io.BytesIO(data))
    return np.array(data.resize(SHAPE))


# Processes preprocessed data for storage
# This probably being hosted on a lambda?
def process(data):
    # Assuming bytes data (remove this line if already array)
    data = np.array(Image.open(io.BytesIO(data)))
    for i, color in enumerate(('red', 'green', 'blue')):
        yield np.dstack([data[..., i]] * 3), {'color': color}
