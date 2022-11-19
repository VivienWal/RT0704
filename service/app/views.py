from flask import Flask
from flask import render_template
import json as j

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world!"

@app.route('/template')
def template():
    return render_template('home.html')

@app.route('/json')
def json():
    return render_template('video.json')

@app.route('/movies')
def movies():
    f = open('video.json')
    data = j.load(f)
    movies = data['films']
    return render_template('movies.html',movies=movies)




app.run(debug=True,host='0.0.0.0', port=9007)
