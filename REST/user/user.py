from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '127.0.0.1'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_json():
   res = make_response(jsonify(users), 200)
   return res


@app.route("/users/<userid>", methods=['GET'])
def get_bookings_by_userid(userid):
    res = 0
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user),200)
    if res == 0:
        return make_response(jsonify({"error":"User not found"}),400)
    return make_response(requests.get(str("http://127.0.0.1:3201/bookings/" + userid)).json(), 200)


@app.route("/movies/<userid>", methods=['GET'])
def get_movies_by_user(userid):
    movies = []
    res = {}
    bookings = requests.get(str("http://127.0.0.1:3201/bookings/" + userid)).json()
    for booking in bookings["bookings"]:
        dates = booking["dates"]
        for date in dates:
            movies.append(date["movies"])
    for movie in movies:
        for element in movie:
            desc = requests.get("http://127.0.0.1:3200/movies/" + element).json()
            res.setdefault("movies", []).append(desc)
    return make_response(jsonify(res), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
