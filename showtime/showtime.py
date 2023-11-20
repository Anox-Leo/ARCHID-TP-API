### gRPC serveur pour le service showtime ###

### Import des librairies. ###
import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json


class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    # Ici on va chercher les données dans le fichier JSON.
    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    ### Fonctions du serveur gRPC ###

    # Fonction pour récupérer un showtime par sa date et son titre.
    def GetShowtimeByDate(self, request, context):
        for time in self.db:
            if time['date'] == request.date:
                print("Date found!")
                return showtime_pb2.ShowtimeData(date=time['date'], movies=time['movies'], )
        return showtime_pb2.ShowtimeData(date="", movies=[])

    # Fonction pour récupérer la liste des showtimes par leur date et leur titre.
    def GetShowtimes(self, request, context):
        for time in self.db:
            yield showtime_pb2.ShowtimeData(date=time['date'], movies=time['movies'])


### Initialisation du serveur gRPC ###
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


### Lancement du serveur gRPC ###
if __name__ == '__main__':
    serve()
