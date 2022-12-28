import requests

url = 'http://10.11.5.177:5000/api/v1/film'

x = requests.post(url,  json={"ajout": {"titre": "test", "annee": 1990, "realisateur": {"nom": "jeaa", "prenom": "pieaa"}, "acteurs": [{"nom": "traa", "prenom": "loaa"},{"nom": "traa", "prenom": "loaa"}]}})

print(x.text)
