from flask import Flask
from flask import render_template
import json as j
import requests

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
def displaymovies() :
    reponse = requests.get ('http://api:5000/movies')
    print(reponse.text)
    movies = reponse.json()


    return render_template('movies.html',movies=movies)




app.run(debug=True,host='0.0.0.0', port=9007)
