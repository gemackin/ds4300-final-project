from .. import aws_utils as aws
import io, numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def get_filenames(version):
    filenames = aws.execute_sql(f"""
    SELECT filename FROM {aws.TABLE_NAME}
    WHERE version = "{version}"
    """)
    return filenames


def get_total_uploads(filenames):
    return len(filenames)


def calculate_rgb_values(filenames):
    rgb_values = np.zeros((3, 256))
    for filename in filenames:
        data = np.array(Image.open(io.BytesIO(data)))
        data = aws.read_s3()
        for i in range(3):
            values, counts = np.unique(data[..., i], return_counts=True)
            rgb_values[i, values.astype(int)] += counts
    return rgb_values


def plot_rgb_histograms(filenames):
    rgb_values = calculate_rgb_values(filenames)
    fig, ax = plt.subplots(3, 1, figsize=(10, 12))
    for i, color in enumerate(('red', 'green', 'blue')):
        ax[i].hist(rgb_values[..., i], bins=256, color=color, alpha=0.7)
        ax[i].set_title(f'{color.title()} Intensity Distribution')
        ax[i].set_xlabel(f'{color.title()} Intensity')
        ax[i].set_ylabel('Frequency')
    fig.tight_layout()
    return fig