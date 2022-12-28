from flask import Flask
from flask import request
from flask import abort
from datetime import datetime
import json as j
import os

app = Flask(__name__)

   
@app.route('/movies')


# with referme le fichier
def movies():
    with open('video.json') as f :
        data = j.load(f)
        movies = data['films']
        return movies

@app.route('/sup',methods=['DELETE'])

def sup() :
    os.remove('video.json')
    return 'succes'

#@app.post ou app.get

@app.route('/add', methods=['POST'])

def add() :
    if not (request.is_json and "proprio" in request.json.keys() and "nom" in request.json["proprio"].keys() and "prenom" in request.json["proprio"].keys()) : 
        abort(400)   
    if os.path.isfile('video.json') :
        abort(409)
    with open('video.json','x') as f :
        dictionaireVideotheque = {
            "proprietaire" : {
                "nom" : request.json["proprio"]["nom"],
                "prenom" : request.json["proprio"]["prenom"]
                },
            "dernere_modif" : datetime.now().strftime('%d/%m/%Y'),
            "films": []
        }
        j.dump(dictionaireVideotheque,f,indent=4)
        return 'succes'

@app.route('/addfilm', methods=['POST'])

def addfilm() :
    if not (request.is_json and "addfilm" in request.json.keys() and "titre" in request.json["addfilm"].keys() and "annee" in request.json["addfilm"].keys() and "realisateur" in request.json["addfilm"].keys() and "nom" in request.json["addfilm"]["realisateur"].keys() and "prenom" in request.json["addfilm"]["realisateur"].keys() and "acteurs" in request.json["addfilm"].keys() and all([set(acteur.keys()) == set(["nom","prenom"]) for acteur in request.json["addfilm"]["acteurs"]])) : 
        abort(400)   
    if not os.path.isfile('video.json') :
        abort(404)
    with open('video.json','r') as f :
        save = j.load(f)
    with open('video.json','w') as f :
        creationFilm = {
            "titre": request.json["addfilm"]["titre"],
            "annee": request.json["addfilm"]["annee"],
            "realisateur": {
                "nom": request.json["addfilm"]["realisateur"]["nom"],
                "prenom": request.json["addfilm"]["realisateur"]["prenom"]
            },
            "acteurs": []
        }
        for acteur in request.json["addfilm"]["acteurs"] :
            creationFilm["acteurs"].append({"nom": acteur["nom"],"prenom": acteur["prenom"]})

        
        save["films"].append(creationFilm)
        j.dump(save,f,indent=4)
        return 'succes'

@app.route('/supfilm', methods=['DELETE']) 

def supfilm() :
    if not (request.is_json and "titre" in request.json.keys()) :
        abort(400)   
    if not os.path.isfile('video.json') :
        abort(404)
    with open('video.json','r') as f :
        save = j.load(f)
        titre = request.json["titre"]
    
    if titre not in [film['titre'] for film in save['films']] :
        abort(404)
    
    save['films'] = list(filter(lambda f : f ['titre'] != titre, save['films']))
   
    with open('video.json','w') as f :
        j.dump(save,f,indent=4)
        return 'succes'
