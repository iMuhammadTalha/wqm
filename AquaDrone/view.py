from django.http import HttpResponse
from django.shortcuts import render
import joblib
#import torch
from django.core.files.storage import default_storage
from PIL import Image
#from keras_model import load_model
#from torchvision import datasets, models, transforms
#from torch.autograd import Variable
import json
import numpy as np
import os

from AquaDrone import settings

from .firebase_helper import get_firebase_data, get_heatmap_data, get_graph_data

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd 
import plotly.offline as pyo

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
    firebase_data = get_graph_data()
    firebase_data_json = json.dumps(firebase_data)

    return render(request, 'firebase_graph.html', {'firebase_data': firebase_data_json})



def heatmap_data_view(request):

    heatmap_image_path = os.path.join(settings.MEDIA_ROOT, 'heat.html')

    if not os.path.exists(heatmap_image_path):
        heatmapData,lat_val,long_val = get_heatmap_data()
    
        # Reshape the 1D array to a 2D array
        # heatmapData = np.reshape(heatmapData, (-1, 1))
        hm_data=np.array(heatmapData)
        lat_data=np.array(lat_val)
        long_data=np.array(long_val)
        df = pd.DataFrame()
        df['Latitude']=lat_data
        df['Longitude']=long_data
        df['Class']=hm_data
        df.head()
        fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Class',
                            mapbox_style="stamen-terrain",
                            color_continuous_scale = ['darkred', 'orange', 'yellow', 'lawngreen', 'green'], title='Heatmap')
    # Create a figure and axes
    
    #fig, ax = plt.subplots()
    #total_elements = len(heatmapData)

    # Find the largest square number less than or equal to the total number of elements
    
    #square_number = int(np.sqrt(total_elements))
    #rows = columns = square_number

    # Calculate the number of elements to drop
    
    #drop_elements = total_elements - (rows * columns)

    # Drop the required number of elements from the end of the array
    
    #dropped_data = heatmapData[:-drop_elements]

    # Reshape the remaining data into a 2D array with the calculated shape
    
    #reshaped_data = np.reshape(dropped_data, (rows, columns))




    # Create the heatmap using seaborn
    #heatmap = sns.heatmap(reshaped_data, annot=True, cmap='crest', cbar=False, vmin=0, vmax=4)
    
    # Set the x and y-axis labels
    #ax.set_xlabel('X-axis')
    #ax.set_ylabel('Y-axis')

    # Set the title of the heatmap
    #ax.set_title('Heatmap')

    # Save the heatmap as an image file
    #plt.savefig(heatmap_image_path)

    # Close the figure to free up resources
    #plt.close(fig)
    if not os.path.exists(heatmap_image_path):
        pyo.plot(fig, filename=heatmap_image_path, auto_open=False)

    return render(request, 'heatmap.html', {'heatmap_image_path': 'heat.html', 'MEDIA_URL': settings.MEDIA_URL})

def main(request):
    return render(request, 'main.html')