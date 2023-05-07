import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import random

import numpy as np
# from keras.models import load_model
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

    # Filter the data to exclude records with a specific column
    filtered_data = [record for record in data if record is not None and ('class' not in record or record['class'] is None)]

    # Add 'class' key with value 1 to each record
    for record in filtered_data:
        temp = (float(record['Temperature']) -  24.258011)/4.548304
        do = (float(record['Oxygen']) - 6.933291)/2.479083
        ph = (float(record['pH']) - 7.474826)/0.582064
        ec = (float(record['Conductivity']) - 4558.724262)/9580.675070
        t = np.array([[temp,do,ph,ec]])
        # Todo
        # savedModel=load_model('./model/WQA_MLP_Model.h5')
        # prob = savedModel.predict(t)
        # pred = prob.argmax(axis=1)
        # out = pred[0]
        # record['class'] = out
        record['Class'] = random.randint(0, 4)

    return data

# Get real-time data from Firebase
def get_heatmap_data():
    ref = db.reference('/UserID: GsjRI430w9hczwcNXiDo9XnNsJo1/0-0|5:0:0')
    data = ref.get()

    # Filter the data to exclude records with a specific column
    filtered_data = [record for record in data if record is not None and ('class' not in record or record['class'] is None)]
    class_values = []  # Array to store the 'class' values

    # Add 'class' key with value 1 to each record
    for record in filtered_data:
        temp = (float(record['Temperature']) -  24.258011)/4.548304
        do = (float(record['Oxygen']) - 6.933291)/2.479083
        ph = (float(record['pH']) - 7.474826)/0.582064
        ec = (float(record['Conductivity']) - 4558.724262)/9580.675070
        t = np.array([[temp,do,ph,ec]])
        # Todo
        # savedModel=load_model('./model/WQA_MLP_Model.h5')
        # prob = savedModel.predict(t)
        # pred = prob.argmax(axis=1)
        # out = pred[0]
        # record['class'] = out
        record['class'] = random.randint(0, 4)
        class_values.append(record['class'])


    return class_values