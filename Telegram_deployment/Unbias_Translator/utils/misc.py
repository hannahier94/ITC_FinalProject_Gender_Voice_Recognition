import tensorflow as tf
from tensorflow.keras.models import load_model
from utils.prepdata import extract_spectrum
import os


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


def User_Directory(user_name):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory_root = PROJECT_ROOT+'\\'+user_name
    if not os.path.exists(directory_root):
        os.makedirs(directory_root)
    return directory_root


def enumerated_filename(directory):
    files = os.listdir(directory)
    if len(files) == 0:
        return '1'
    else:
        files = [int(file.split('.')[0]) for file in files]
        return str(max(files)+1)