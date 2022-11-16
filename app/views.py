from flask import render_template
from app import app 

@app.route('/')
def home():
    return "Hello world!"

@app.route('/template')
def template():
    return render_template('home.html')

@app.route('/json')
def json():
    return render_template('video.json')