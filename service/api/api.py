from flask import Flask
from flask import request
from flask import abort
from datetime import datetime
import json as j
import os
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


@app.route('/api/v1/film',methods=['GET'])

# with referme le fichier
def movies():
    with open('video.json') as f :
        data = j.load(f)
        movies = data['films']
        #return j.dumps(movies,indent=4)
        return movies

@app.route('/api/v1/proprietaire',methods=['GET'])

# with referme le fichier
def proprietaire():
    with open('video.json') as f :
        data = j.load(f)
        proprietaire = data['proprietaire']
        return proprietaire

@app.route('/api/v1/information',methods=['GET'])

# with referme le fichier
def information():
    with open('video.json') as f :
        data = j.load(f)
        information = data['dernere_modif']
        return information

@app.route('/api/v1/supvideotheque',methods=['DELETE'])

def supvideotheque() :
    os.remove('video.json')
    return 'succes'

#@app.post ou app.get

@app.route('/api/v1/videotheque', methods=['POST'])

def videotheque() :
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

@app.route('/api/v1/film', methods=['POST'])

def film() :
    if request.is_json and "ajout" in request.json.keys() and "titre" in request.json["ajout"].keys() :

        if not ("annee" in request.json["ajout"].keys() and "realisateur" in request.json["ajout"].keys() and "nom" in request.json["ajout"]["realisateur"].keys() and "prenom" in request.json["ajout"]["realisateur"].keys() and "acteurs" in request.json["ajout"].keys() and all([set(acteur.keys()) == set(["nom","prenom"]) for acteur in request.json["ajout"]["acteurs"]])) :
            abort(400)
        if not os.path.isfile('video.json') :
            abort(404)
        with open('video.json','r') as f :
            save = j.load(f)
    #boucle pour titre film
        for film in save["films"] :
            if film["titre"] == request.json["ajout"]["titre"] :
                abort(400)
        with open('video.json','w') as f :
            nom_real = request.json["ajout"]["realisateur"]["nom"]
            prenom_real = request.json["ajout"]["realisateur"]["prenom"]
            if not nom_real:
                nom_real = "/"
            if not prenom_real:
                prenom_real = "/"

            creationFilm = {
                "titre": request.json["ajout"]["titre"],
                "annee": request.json["ajout"]["annee"],
                "realisateur": {
                    "nom": nom_real,
                    "prenom": prenom_real
                },
                "acteurs": []
            }
            for acteur in request.json["ajout"]["acteurs"] :
                creationFilm["acteurs"].append({"nom": acteur["nom"],"prenom": acteur["prenom"]})

            save["dernere_modif"] = datetime.now().strftime('%d/%m/%Y')
            save["films"].append(creationFilm)
            j.dump(save,f,indent=4)
            return 'succes'

    elif request.is_json and "recherche" in request.json.keys() and "titre" in request.json["recherche"].keys() :
        with open('video.json','r') as f :
            save = j.load(f)
    #boucle pour titre film
        for film in save["films"] :
            if film["titre"].lower() == request.json["recherche"]["titre"].lower() :
                return j.dumps(film)
        abort(400)
    elif request.is_json and "recherche" in request.json.keys() and "nom_acteur" in request.json["recherche"].keys() :
        with open('video.json','r') as f :
            save = j.load(f)
        response = []
        for film in save["films"] :
            for acteur in film["acteurs"] :
                if acteur["nom"].lower() == request.json["recherche"]["nom_acteur"].lower() :
                    response.append(film)
        if response :
            return j.dumps(response)
        else :
            abort(400)
    elif request.is_json and "modification" in request.json.keys() and "titre" in request.json["modification"].keys() and "data" in request.json.keys() :
        with open('video.json','r') as f :
            save = j.load(f)
        response = {}
        responsetotal = []
        for film in save["films"] :
            if film["titre"].lower() == request.json["modification"]["titre"].lower() :
                for key in film :
                    if key in request.json["data"].keys() :
                        response[key]=request.json["data"][key]
                    else :
                        response[key]=film[key]
            else :
                responsetotal.append(film)
        with open('video.json','w') as f :
            save["dernere_modif"] = datetime.now().strftime('%d/%m/%Y')
            save["films"] = responsetotal
            save["films"].append(response)
            j.dump(save,f,indent=4)
            return 'succes'
    else :
        abort(400)



@app.route('/api/v1/film', methods=['DELETE'])

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

    save["dernere_modif"] = datetime.now().strftime('%d/%m/%Y')
    save['films'] = list(filter(lambda f : f ['titre'] != titre, save['films']))

    with open('video.json','w') as f :
        j.dump(save,f,indent=4)
        return 'succes'
