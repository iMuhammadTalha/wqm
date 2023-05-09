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

import plotly.offline as pyo
import plotly.express as px
import pandas as pd 

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
    heatmapData,lat_val,long_val = get_heatmap_data()

    hm_data=np.array(heatmapData)
    lat_data=np.array(lat_val)
    long_data=np.array(long_val)
    df = pd.DataFrame()
    df['Latitude']=lat_data
    df['Longitude']=long_data
    df['Class_pred']=hm_data
    df.head()
    fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Class_pred',
                        mapbox_style="stamen-terrain")
    
    heatmap_image_path = os.path.join(settings.MEDIA_ROOT, 'heat.html')

    pyo.plot(fig, filename=heatmap_image_path)

    return render(request, 'heatmap.html', {'heatmap_image_path': heatmap_image_path, 'MEDIA_URL': settings.MEDIA_URL})


def main(request):
    return render(request, 'main.html')