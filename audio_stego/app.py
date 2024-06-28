from flask import Flask, render_template, request, redirect, url_for
import os
from audio_steganography import em_audio, ex_msg

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hideWave')
def hideWave():
    return render_template('hideWave.html')

@app.route('/exWave')
def exWave():
    return render_template('exWave.html')

@app.route('/hide_message', methods=['POST'])
def hide_message():
    audiofile = request.files['audiofile']
    secretmsg = request.form['secretmsg']
    audiofile_path = os.path.join(UPLOAD_FOLDER, audiofile.filename)
    outputfile_name = 'hidden_' + audiofile.filename
    outputfile_path = os.path.join(OUTPUT_FOLDER, outputfile_name)
    audiofile.save(audiofile_path)
    
    result = em_audio(audiofile_path, secretmsg, outputfile_path)
    return render_template('hideWave.html', result=result)

@app.route('/extract_message', methods=['POST'])
def extract_message():
    audiofile = request.files['audiofile']
    audiofile_path = os.path.join(UPLOAD_FOLDER, audiofile.filename)
    audiofile.save(audiofile_path)
    
    result = ex_msg(audiofile_path)
    return render_template('exWave.html', extracted_message=result)

if __name__ == '__main__':
    app.run(debug=True)
