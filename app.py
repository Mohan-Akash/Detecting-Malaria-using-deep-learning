﻿from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/my_model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
print('Model loaded. Start serving...')

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(50, 50))  # Target size must agree with what the trained model expects!!

    # Preprocessing the image
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # Predicting the class
    preds = model.predict(img)
    pred = np.argmax(preds, axis=1)
    return pred

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        pred = model_predict(file_path, model)
        os.remove(file_path)  # Removes file from the server after prediction has been returned

        # Arrange the correct return according to the model
        str1 = 'Malaria Parasitized'
        str2 = 'Normal'
        if pred[0] == 0:
            return str1
        else:
            return str2
    return None

if __name__ == '__main__':
    app.run()