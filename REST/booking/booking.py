from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from types import SimpleNamespace
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '127.0.0.1'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
   res = make_response(jsonify(bookings), 200)
   return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    res = {}
    for user in bookings:
        if str(user["userid"]) == str(userid):
            res.setdefault("bookings", []).append(user)
    if len(res) == 0:
        return make_response(jsonify({"error":"User not found"}),400)
    else:
        return make_response(jsonify(res),200)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()
    schedule = requests.get("http://127.0.0.1:3202/showtimes").json()
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
    res = make_response(jsonify({"message":"booking added"}),200)
    return res


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
