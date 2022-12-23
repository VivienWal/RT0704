import requests

url = 'http://10.11.5.177:5000/addfilm'

x = requests.post(url,  json={"addfilm": {"titre": "test", "annee": 1990, "realisateur": {"nom": "jean", "prenom": "pierre"}, "acteurs": [{"nom": "troll", "prenom": "loulilou"},{"nom": "trol2l", "prenom": "loulilo2u"}]}})

print(x.text)
