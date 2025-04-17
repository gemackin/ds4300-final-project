import io, numpy as np, pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
# Attempting to import beyond top-level package
import sys, os
sys.path.append(os.path.abspath('.'))
import aws_utils as aws # Can't do "from" when uninitialized


# Returns the S3 paths of files uploaded
def get_filenames(version):
    def format_filename(filename, directory, **kws):
        return os.path.join(directory, filename)
    response = aws.execute_sql(f"""
    SELECT filename, directory
    FROM {os.environ['RDS_TABLE_NAME']}
    WHERE version = '{version}'
    """)
    return list(map(lambda x: format_filename(**x), response))


# Returns the number of files uploaded
def get_total_uploads(filenames):
    return len(filenames)


# Calculates the RGB histogram bin counts
def calculate_rgb_values(filenames):
    rgb_values = np.zeros((3, 256))
    for filename in filenames:
        data = aws.read_s3(filename)
        data = np.array(Image.open(io.BytesIO(data)))
        for i in range(3):
            values, counts = np.unique(data[..., i], return_counts=True)
            rgb_values[i, values.astype(int)] += counts
    return rgb_values


# Plots the RGB intensity distributions
def plot_rgb_histograms(filenames):
    rgb_values = calculate_rgb_values(filenames)
    fig, ax = plt.subplots(3, 1, figsize=(10, 12))
    for i, color in enumerate(('red', 'green', 'blue')):
        if filenames: # Don't do this if there are no files
            ax[i].bar(range(256), rgb_values[i], width=1, color=color,
                      alpha=0.7, edgecolor='k', linewidth=0.2)
        ax[i].set_title(f'{color.title()} Intensity Distribution')
        ax[i].set_xlabel(f'{color.title()} Intensity')
        ax[i].set_ylabel('Frequency')
        ax[i].set_xlim(0.5, 255.5)
    fig.tight_layout()
    return fig