from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np 
from utils.prepdata import extract_spectrum

def open_model(filename="best_model_final.h5"):
    """ Given filename, returns the model
    param filename: filepath for model
    return : pretrained model """
    with tf.device("/cpu:0"):
        model = load_model(filename)
    return model

def predict(X, model):
    """ Given X, returns a prediction
    param X: the feature values to consider
    returns pred_pickle: the prediction """

    X = extract_spectrum(X).reshape(-1,54,128,1)
    with tf.device("/cpu:0"):
        pred = model.predict(X)
        if pred[0][0] <= 0.5:
            return 'female'
        else:
            return 'male'

def check_file(name, allowed):
    """ Checks that file was uploaded with a name 
    and proper extension
    param name: name to check
    returns: boolean (False if file is corrupt)"""
    
    if name == '':
        return False

    if '.' not in name:
        return False

    ext = name.split('.')[-1]

    if ext.lower() not in allowed:
        return False
    return True

