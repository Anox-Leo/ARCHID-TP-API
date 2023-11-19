### gRPC serveur pour le service booking ###

import json
from concurrent import futures

### Import des librairies. ###
import grpc

import booking_pb2
import booking_pb2_grpc
from showtime.client import showtime_pb2_grpc


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
                print("Booking found!")
                for dates in booking['dates']:
                    return booking_pb2.BookingData(id=booking['userid'], date=dates['date'], movies=dates['movies'])
        return booking_pb2.BookingData(id="", date="", movies=[])

    # Fonction pour récupérer tous les utilisateurs.
    def GetBookings(self, request, context):
        for booking in self.db:
            for dates in booking['dates']:
                yield booking_pb2.BookingData(id=booking['userid'], date=dates['date'], movies=dates['movies'])


### Initialisation du serveur gRPC ###
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    times_channel = grpc.insecure_channel('localhost:3005')  # Assurez-vous que le port est correct
    times_stub = showtime_pb2_grpc.TimesStub(times_channel)

    # Initialisation de BookingServicer avec le stub Times
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(times_stub), server)
    server.add_insecure_port('[::]:3004')
    server.start()
    server.wait_for_termination()


### Lancement du serveur gRPC ###
if __name__ == '__main__':
    serve()
