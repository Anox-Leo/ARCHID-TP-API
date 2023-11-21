### User service ###

### Import des librairies. ###
from flask import Flask, jsonify, make_response
import requests
import json

### Initialisation du serveur Flask ###
app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

### Ici on va chercher les données dans le fichier JSON. ###
with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


### Initialisation des routes ###

# Route pour la page d'accueil.
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# Route pour récupérer tout les utilisateurs.
@app.route("/users", methods=['GET'])
def get_json():
    res = make_response(jsonify(users), 200)
    return res


# Route pour récupérer un utilisateur par son id.
@app.route("/users/<userid>", methods=['GET'])
def get_bookings_by_userid(userid):
    res = 0
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
    if res == 0:
        return make_response(jsonify({"error": "User not found"}), 400)
    return make_response(requests.get(str("http://booking:3201/bookings/" + userid)).json(), 200)


# Route pour récupérer les films d'un utilisateur par son id.
@app.route("/movies/<userid>", methods=['GET'])
def get_movies_by_user(userid):
    movies = []
    res = {}
    bookings = requests.get(str("http://booking:3201/bookings/" + userid)).json()
    for booking in bookings["bookings"]:
        dates = booking["dates"]
        for date in dates:
            movies.append(date["movies"])
    for movie in movies:
        for element in movie:
            desc = requests.get("http://movie:3200/movies/" + element).json()
            res.setdefault("movies", []).append(desc)
    return make_response(jsonify(res), 200)


### Lancement du serveur Flask ###
if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
