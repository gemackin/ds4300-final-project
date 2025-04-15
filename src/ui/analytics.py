import pandas as pd
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def load_data(csv_path='uploaded_data.csv'):
    """Load saved metadata from image uploads."""
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['filename', 'description', 'dominant_color'])

def get_total_uploads(data):
    return len(data)

def get_most_common_colors(data, top_n=5):
    counter = Counter(data['dominant_color'].dropna())
    common = counter.most_common(top_n)
    return pd.DataFrame(common, columns=['color', 'count'])

def extract_dominant_color(image_path):
    """Extract the most common color from the image as an RGB tuple."""
    try:
        image = Image.open(image_path)
        image = image.resize((100, 100))  
        pixels = list(image.getdata())
        counter = Counter(pixels)
        dominant_color = counter.most_common(1)[0][0]
        return f"rgb{dominant_color}"
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def plot_rgb_histograms(data):
    """Plot histograms for Red, Green, and Blue color channels separately."""
    red_values = []
    green_values = []
    blue_values = []

    # Extract RGB values from dominant colors
    for color in data['dominant_color'].dropna():
        try:
            if color.startswith("rgb"):
                rgb_values = tuple(map(int, color[4:-1].split(",")))
                red_values.append(rgb_values[0])
                green_values.append(rgb_values[1])
                blue_values.append(rgb_values[2])
            elif color.startswith("#"):
                rgb_values = mcolors.hex2color(color)
                red_values.append(int(rgb_values[0] * 255))
                green_values.append(int(rgb_values[1] * 255))
                blue_values.append(int(rgb_values[2] * 255))
        except Exception as e:
            print(f"Error processing color {color}: {e}")
            continue

    # Plot histograms for R, G, B channels
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # Red histogram
    axs[0].hist(red_values, bins=25, color='red', alpha=0.7)
    axs[0].set_title('Red Intensity Distribution')
    axs[0].set_xlabel('Red Intensity')
    axs[0].set_ylabel('Frequency')

    # Green histogram
    axs[1].hist(green_values, bins=25, color='green', alpha=0.7)
    axs[1].set_title('Green Intensity Distribution')
    axs[1].set_xlabel('Green Intensity')
    axs[1].set_ylabel('Frequency')

    # Blue histogram
    axs[2].hist(blue_values, bins=25, color='blue', alpha=0.7)
    axs[2].set_title('Blue Intensity Distribution')
    axs[2].set_xlabel('Blue Intensity')
    axs[2].set_ylabel('Frequency')

    plt.tight_layout()
    return fig