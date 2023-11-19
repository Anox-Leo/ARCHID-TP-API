### REST API pour le service User ###

### Import des librairies ###
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
from concurrent import futures

# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

### Initialisation du serveur Flask ###

app = Flask(__name__)

# Port d'écoute du serveur.
PORT = 3003

# Nom d'hôte du serveur.
HOST = 'localhost'

# Ici on va chercher les données dans le fichier JSON.
with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


### Routes du serveur Flask ###

# Route par défaut.
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# Route pour récupérer tous les utilisateurs.
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
    return make_response(requests.get("http://172.16.137.162:3201/bookings/chris_rivers").json(), 200)


# Route pour récupérer les films d'un utilisateur par son id.
@app.route("/movies/<userid>", methods=['GET'])
def get_movies_by_user(userid):
    movies = []
    res = {}
    bookings = requests.get("http://172.16.137.162:3201/bookings/chris_rivers").json()
    for booking in bookings["bookings"]:
        dates = booking["dates"]
        for date in dates:
            movies.append(date["movies"])
    for movie in movies:
        for element in movie:
            query = 'query { movie_with_id(_id: "' + element + '") { id rating title director } }'
            desc = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
            res.setdefault("movies", []).append(desc)
    return make_response(jsonify(res), 200)


### Lancement du serveur Flask ###

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
