### Showtime service ###

### Import des librairies. ###
from flask import Flask, jsonify, make_response
import json

### Initialisation du serveur Flask ###
app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

### Ici on va chercher les données dans le fichier JSON. ###
with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


### Initialisation des routes ###

# Route pour la page d'accueil.
@app.route("/", methods=['GET'])
def home():
    return "<h1Test</h1>"


# Route pour récupérer toutes les séances.
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    res = make_response(jsonify(schedule), 200)
    return res


# Route pour récupérer une séance par sa date.
@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    for time in schedule:
        if str(time["date"]) == str(date):
            res = make_response(jsonify(time), 200)
            return res
    return make_response(jsonify({"error": "Date not found"}), 400)


### Lancement du serveur Flask ###
if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
