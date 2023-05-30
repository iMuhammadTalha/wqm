import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import random

import numpy as np
from keras.models import load_model
# Todo

# Initialize Firebase app
# Get the path to the JSON file
file_path = os.path.join(os.path.dirname(__file__), 'firebase_key.json')

cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aquadrone-linkweb-default-rtdb.firebaseio.com/'
})

# Get real-time data from Firebase
def get_firebase_data():
    ref = db.reference('/UserID: GsjRI430w9hczwcNXiDo9XnNsJo1/0-0|5:0:0')
    data = ref.get()
    data = [record for record in data if record is not None]
    
    # Filter the data to exclude records with a specific column
    filtered_data = [record for record in data if record is not None and ('class' not in record or record['class'] is None)]

    w = np.array([0.1398697291738087, 0.411381556393555, 0.4370929036681522, 0.011655810764484058])


    # Add 'class' key with value 1 to each record
    for record in filtered_data:
        temp = float(record['Temperature'])
        if temp <= 0:
            temp = 100
        elif temp > 0 and temp <= 5:
            temp = 80
        elif temp > 5 and temp <= 10:
            temp = 60
        elif temp > 10 and temp <= 15:
            temp = 40
        else:
            temp = 0
        do = float(record['Oxygen'])
        if do > 7:
            do = 100
        elif do > 5 and temp <= 7:
            do = 80
        elif do > 4 and do <= 5:
            do = 60
        elif do > 3 and temp <= 4:
            do = 40
        else:
            do = 0 
        ph = float(record['pH'])
        if (ph > 7 and ph <= 8.5):
            ph = 100
        elif (ph > 8.5 and ph <= 8.7) or (ph > 6.8 and ph <= 6.9):
            ph = 80
        elif (ph > 8.7 and ph <= 8.9) or (ph > 6.7 and ph <= 6.8):
            ph = 60
        elif (ph > 8.9 and ph <= 9.2) or (ph > 6.5 and ph <= 6.7):
            ph = 40
        elif (ph > 9.2 or ph <= 6.5):
            ph = 0
        ec = float(record['Conductivity'])
        if ec < 75:
            ec = 100
        elif ec > 75 and ec <= 150:
            ec = 80
        elif ec > 150 and ec <= 225:
            ec = 60
        elif ec > 225 and ec <= 300:
            ec = 40
        else:
            ec = 0
        t = np.array([temp,do,ph,ec])
        # Todo
        WQI=0
        for i in range (4):
            WQI = WQI + w[i]*t[i]
        WQI = round(WQI,2)
        record['WQI'] = float(WQI)
        #print(record['class'])
        #record['Class'] = random.randint(0, 4)

    return data

# Get real-time data from Firebase
def get_graph_data():
    ref = db.reference('/UserID: GsjRI430w9hczwcNXiDo9XnNsJo1/0-0|5:0:0')
    data = ref.get()
    data = [record for record in data if record is not None]
    
    # Filter the data to exclude records with a specific column
    filtered_data = [record for record in data if record is not None and ('class' not in record or record['class'] is None)]

    # Add 'class' key with value 1 to each record
    for record in filtered_data:
        temp = (float(record['Temperature']) -  24.258011)/4.548304
        do = (float(record['Oxygen']) - 6.933291)/2.479083
        ph = (float(record['pH']) - 7.474826)/0.582064
        ec = (float(record['Conductivity']) - 4558.724262)/9580.675070
        t = np.array([[temp,do,ph,ec]])
        
    return data

# Get real-time data from Firebase
def get_heatmap_data():
    ref = db.reference('/UserID: GsjRI430w9hczwcNXiDo9XnNsJo1/0-0|5:0:0')
    data = ref.get()

    # Filter the data to exclude records with a specific column
    filtered_data = [record for record in data if record is not None and ('class' not in record or record['class'] is None)]
    class_values = []  # Array to store the 'class' values
    lat_values = []
    long_values = []
    # Add 'class' key with value 1 to each record
    for record in filtered_data:
        temp = (float(record['Temperature']) -  24.258011)/4.548304
        do = (float(record['Oxygen']) - 6.933291)/2.479083
        ph = (float(record['pH']) - 7.474826)/0.582064
        ec = (float(record['Conductivity']) - 4558.724262)/9580.675070
        t = np.array([[temp,do,ph,ec]])
        # Todo
        savedModel=load_model('./model/WQA_MLP_Model.h5')
        prob = savedModel.predict(t)
        pred = prob.argmax(axis=1)
        out = pred[0]
        record['class'] = out
        #record['class'] = random.randint(0, 4)
        class_values.append(float(record['class']))
        lat_values.append(float(record['Latitude']))
        long_values.append(float(record['Longitude']))

    return class_values, lat_values,long_values