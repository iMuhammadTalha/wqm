from django.http import HttpResponse
from django.shortcuts import render
import joblib
import torch
from django.core.files.storage import default_storage
from PIL import Image
from torchvision import datasets, models, transforms
from torch.autograd import Variable
import json
import numpy as np
import os

from AquaDrone import settings

from .firebase_helper import get_firebase_data, get_heatmap_data

import seaborn as sns
import matplotlib.pyplot as plt

test_image1 = "image12.png"

def index(request):
    return render(request, 'index.html')

def publications(request):
    return render(request, 'publications.html')

def team(request):
    return render(request, 'team.html')


def firebase_data_view(request):
    firebase_data = get_firebase_data()
    return render(request, 'firebase_data.html', {'firebase_data': firebase_data})

def firebase_graph_view(request):
    firebase_data = get_firebase_data()
    firebase_data_json = json.dumps(firebase_data)

    return render(request, 'firebase_graph.html', {'firebase_data': firebase_data_json})

def heatmap_data_view(request):
    heatmapData = get_heatmap_data()
    
    # Reshape the 1D array to a 2D array
    # heatmapData = np.reshape(heatmapData, (-1, 1))

    # Create a figure and axes
    fig, ax = plt.subplots()

    total_elements = len(heatmapData)

    # Find the largest square number less than or equal to the total number of elements
    square_number = int(np.sqrt(total_elements))
    rows = columns = square_number

    # Calculate the number of elements to drop
    drop_elements = total_elements - (rows * columns)

    # Drop the required number of elements from the end of the array
    dropped_data = heatmapData[:-drop_elements]

    # Reshape the remaining data into a 2D array with the calculated shape
    reshaped_data = np.reshape(dropped_data, (rows, columns))




    # Create the heatmap using seaborn
    heatmap = sns.heatmap(reshaped_data, annot=True, cmap='crest', cbar=False, vmin=0, vmax=4)
    
    # Set the x and y-axis labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # Set the title of the heatmap
    ax.set_title('Heatmap')

    # Save the heatmap as an image file
    heatmap_image_path = os.path.join(settings.MEDIA_ROOT, 'heatmap.png')
    plt.savefig(heatmap_image_path)

    # Close the figure to free up resources
    plt.close(fig)

    return render(request, 'heatmap.html', {'heatmap_image_path': heatmap_image_path, 'MEDIA_URL': settings.MEDIA_URL})

def main(request):
    return render(request, 'main.html')