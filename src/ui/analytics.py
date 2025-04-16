import io, numpy as np
from PIL import Image
from matplotlib import pyplot as plt
# Attempting to import beyond top-level package
import sys, os
sys.path.append(os.path.abspath('.'))
import aws_utils as aws # Can't do "from" when uninitialized


# Returns the S3 paths of files uploaded
def get_filenames(version):
    filenames = aws.execute_sql(f"""
    SELECT filename, directory
    FROM {os.environ['RDS_TABLE_NAME']}
    WHERE version = "{version}"
    """)
    print(filenames) # TESTING
    return filenames


# Returns the number of files uploaded
def get_total_uploads(filenames):
    return len(filenames)


# Calculates the RGB histogram bin counts
def calculate_rgb_values(filenames):
    rgb_values = np.zeros((3, 256))
    for filename in filenames:
        data = np.array(Image.open(io.BytesIO(data)))
        data = aws.read_s3()
        for i in range(3):
            values, counts = np.unique(data[..., i], return_counts=True)
            rgb_values[i, values.astype(int)] += counts
    return rgb_values


# Plots the RGB intensity distributions
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