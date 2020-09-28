import numpy as np
from flask import Flask, request
from utils.prepdata import extract_spectrum
from utils.prepaudio import get_large_audio_transcription
from utils.analyzetext import determine_tense_input
from utils.TranslateOutput import get_translation
from utils.misc import check_file, predict, open_model
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, send_from_directory
import json
from tensorflow.keras.models import load_model
import tensorflow as tf
import os

EXTS = ['wav', 'mp3']
UPLOAD_FOLDER = './uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

app = Flask(__name__, template_folder='templates/public/') 
    
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = EXTS


model = open_model()


def invoke_pipeline(audiofile):
    loc = './uploads/' + audiofile.filename
    pred = predict(loc, model=open_model())
    text = get_large_audio_transcription(audiofile)
    split_sentence = determine_tense_input(text)
    res = get_translation(split_sentence, pred)
    return res


@app.route('/')
def enter():
    return 'Welcome!'


@app.route('/results')
def display_res(text):
    return text


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":

        if request.files:
            
            newfile = request.files["audio"]
            
            if not check_file(newfile.filename, \
                              allowed = app.config['ALLOWED_EXTENSIONS']):
                return redirect(request.url)
            
            newfile.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                      newfile.filename))
            
            return invoke_pipeline(newfile)
    return render_template('upload.html')


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = os.environ.get('PORT')

    if port:
        # 'PORT' variable exists - running on Heroku, listen on external IP and on given by Heroku port
        app.run(host='0.0.0.0', port=int(port))
    else:
        # 'PORT' variable doesn't exist, running not on Heroku, presumabely running locally, run with default
        #   values for Flask (listening only on localhost on default Flask port)
        app.run(port=5000)