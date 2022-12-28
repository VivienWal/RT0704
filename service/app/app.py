from flask import Flask
from flask import render_template
import json as j
import requests



app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')



@app.route('/')
def home():
    response = requests.get('http://10.11.5.177:5000/api/v1/film')
    response2 = requests.get('http://10.11.5.177:5000/api/v1/proprietaire')
    response3 = requests.get('http://10.11.5.177:5000/api/v1/information')
    film = response.json()
    proprietaire = response2.json()
    information = response3.text
    
    return render_template('index.html',test=film,test2=proprietaire,test3=information)

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
