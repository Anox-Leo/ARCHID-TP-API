### gRPC serveur pour le service booking ###

import json
from concurrent import futures

### Import des librairies. ###
import grpc

import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):

    # Ici on va chercher les données dans le fichier JSON.
    def __init__(self, times_stub):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

            # Stub pour Times
            self.times_stub = times_stub

    ### Fonctions du serveur gRPC ###

    # Fonction pour récupérer un utilisateur par son id.
    def GetBookingByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id:
                for dates in booking['dates']:
                    yield booking_pb2.BookingResponse(id=booking['userid'], date=dates['date'], movies=dates['movies'])

    # Fonction pour récupérer tous les utilisateurs.
    def GetBookings(self, request, context):
        for booking in self.db:
            for dates in booking['dates']:
                yield booking_pb2.BookingResponse(id=booking['userid'], date=dates['date'], movies=dates['movies'])

    def CreateBooking(self, request, context):
        schedule = self.times_stub.GetShowtimeByDate(showtime_pb2.Date(date=request.date))
        movies = []
        if len(schedule.movies) == 0 or request.movieid not in schedule.movies:
            return booking_pb2.BookingResponse(id="", date="", movies=[])
        else:
            movies.append(request.movieid)
            self.db.append({
                "userid": request.id,
                "dates": [
                    {
                        "date": request.date,
                        "movies": movies,
                    }
                ]
            })
            return booking_pb2.BookingResponse(id=request.id, date=request.date, movies=movies)


### Initialisation du serveur gRPC ###
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    times_channel = grpc.insecure_channel('localhost:3002')
    times_stub = showtime_pb2_grpc.ShowtimeStub(times_channel)

    # Initialisation de BookingServicer avec le stub Times
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(times_stub), server)
    server.add_insecure_port('[::]:3004')
    server.start()
    server.wait_for_termination()


### Lancement du serveur gRPC ###
if __name__ == '__main__':
    serve()
