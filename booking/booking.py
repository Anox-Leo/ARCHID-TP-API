### gRPC serveur pour le service booking ###

### Import des librairies. ###
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json


class BookingServicer(booking_pb2_grpc.BookingServicer):

    # Ici on va chercher les données dans le fichier JSON.
    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

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
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3004')
    server.start()
    server.wait_for_termination()


### Lancement du serveur gRPC ###
if __name__ == '__main__':
    serve()
