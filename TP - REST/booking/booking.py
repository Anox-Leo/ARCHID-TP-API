### Booking service ###

### Import des librairies. ###
from flask import Flask, request, jsonify, make_response
import requests
import json

### Initialisation du serveur Flask ###
app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

### Ici on va chercher les données dans le fichier JSON. ###
with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


### Initialisation des routes ###

# Route pour la page d'accueil.
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# Route pour récupérer toutes les réservations.
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


# Route pour récupérer une réservation par son l'id d'un User.
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    res = {}
    for user in bookings:
        if str(user["userid"]) == str(userid):
            res.setdefault("bookings", []).append(user)
    if len(res) == 0:
        return make_response(jsonify({"error": "User not found"}), 400)
    else:
        return make_response(jsonify(res), 200)


# Route pour ajouter une réservation à un User.
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()
    schedule = requests.get("http://showtime:3202/showtimes").json()
    find = False

    for time in schedule:
        if str(time["date"]) == req["date"]:
            if req["movieid"] in time["movies"]:
                find = True

    if not find:
        return make_response(jsonify({"error": "Film for this date not found"}), 400)

    bookings.append({
        "userid": userid,
        "dates": [
            {
                "date": req["date"],
                "movies": [
                    req["movieid"]
                ]
            }
        ]
    })
    res = make_response(jsonify({"message": "booking added"}), 200)
    return res


### Lancement du serveur Flask ###
if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
