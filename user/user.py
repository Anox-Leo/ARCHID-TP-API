### TP - REST API pour le service User ###

### Import des librairies ###
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

from google.protobuf.json_format import MessageToDict

# CALLING gRPC requests
import grpc
from concurrent import futures

import booking_pb2
import booking_pb2_grpc


# CALLING GraphQL requests

### Initialisation du serveur Flask ###

app = Flask(__name__)

# Port d'écoute du serveur.
PORT = 3003

# Nom d'hôte du serveur.
HOST = 'localhost'

# Ici on va chercher les données dans le fichier JSON.
with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]

    # Connexion au serveur gRPC de Booking
    booking_channel = grpc.insecure_channel('localhost:3004')
    booking_stub = booking_pb2_grpc.BookingStub(booking_channel)


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
    user_found = next((user for user in users if str(user["id"]) == str(userid)), None)
    if user_found:
        # Appel de la procédure distante gRPC pour obtenir les réservations de l'utilisateur
        booking_request = booking_pb2.UserId(id=userid)
        booking_response = booking_stub.GetBookingByUserId(booking_request)

        bookings = {
            "id": userid,
            "dates": []
        }
        for booking in booking_response:
            booking_dict = MessageToDict(booking)
            bookings["dates"].append({
                "date": booking_dict["date"],
                "movies": booking_dict["movies"]
            })

        return make_response(jsonify(bookings), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 400)


# Route pour récupérer les films d'un utilisateur par son id.
@app.route("/movies/<userid>", methods=['GET'])
def get_movies_by_user(userid):
    user_found = next((user for user in users if str(user["id"]) == str(userid)), None)
    if user_found:
        # Appel de la procédure distante gRPC pour obtenir les réservations de l'utilisateur.
        booking_request = booking_pb2.UserId(id=userid)
        booking_response = booking_stub.GetBookingByUserId(booking_request)

        dates = []

        for booking in booking_response:
            booking_dict = MessageToDict(booking)
            dates.append({
                "date": booking_dict["date"],
                "movies": booking_dict["movies"]
            })

        movies = []
        res = []

        for date in dates:
            for movie in date["movies"]:
                movies.append(movie)
        for element in movies:
            query = 'query { movie_with_id(_id: "' + element + '") { id rating title director } }'
            desc = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
            res.append(desc["data"]["movie_with_id"])

        return make_response(jsonify(res), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 400)


# Route pout récupérer un film par son id.
@app.route("/movies/movie/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    query = 'query {movie_with_id(_id: "' + movieid + '") { id rating title director } }'
    res = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
    return res


# Route pour récupérer un film par son titre.
@app.route("/movies/title/<title>", methods=['GET'])
def get_movie_bytitle(title):
    query = 'query { movie_with_title(_title: "' + title + '") { id rating title director } }'
    res = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
    return res


# Route pour récupérer toutes les réservations.
@app.route("/bookings", methods=['GET'])
def get_bookings():
    # Appel de la procédure distante gRPC pour obtenir les réservations de l'utilisateur.
    booking_request = booking_pb2.BookingEmpty()
    booking_response = booking_stub.GetBookings(booking_request)

    bookings = []
    for booking in booking_response:
        booking_dict = MessageToDict(booking)
        bookings.append({
            "id": booking_dict["id"],
            "date": booking_dict["date"],
            "movies": booking_dict["movies"]
        })

    return make_response(jsonify(bookings), 200)


# Route pour ajouter une réservation à un utilisateur.
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    user_found = next((user for user in users if str(user["id"]) == str(userid)), None)
    if user_found:
        req = request.get_json()
        booking_request = booking_pb2.BookingRequest(id=userid, date=req["date"], movieid=req["movieid"])
        booking_response = booking_stub.CreateBooking(booking_request)

        if booking_response.id == "":
            return make_response(jsonify({"error": "Film for this date not found"}), 400)
        else:
            print(booking_response)
            return make_response(jsonify({"message": "booking added"}), 200)


# Route pour créer un nouveau film.
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()
    query = 'mutation { create_new_movie(_id: "' + movieid + '", _title: "' + req["title"] + '", _director: "' + req[
        "director"] + '", _rating: ' + str(req["rating"]) + ') { id title director rating } }'
    res = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
    return res


# Route pour mettre à jour la note d'un film.
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie(movieid, rate):
    query = 'mutation { update_movie_rate(_id: "' + movieid + '", _rating: ' + str(rate) + ') { id title director rating } }'
    res = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
    return res


# Route pour supprimer un film.
@app.route("/movies/<movieid>", methods=['DELETE'])
def delete_movie(movieid):
    query = 'mutation { delete_movie(_id: "' + movieid + '") { id title director rating } }'
    res = requests.post("http://localhost:3001/graphql", json={'query': query}).json()
    return res


### Lancement du serveur Flask ###

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
