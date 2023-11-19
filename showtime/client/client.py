### Client pour le service Showtime ###

### Import des modules nécessaires ###
import grpc
import showtime_pb2
import showtime_pb2_grpc


### Fonctions du client gRPC###

# Fonction pour récupérer un showtime par sa date.
def get_showtime_by_date(stub, date):
    showtime = stub.GetShowtimeByDate(date)
    print(showtime)


# Fonction pour récupérer tous les showtimes.
def get_list_showtimes(stub):
    allshowtimes = stub.GetShowtimes(showtime_pb2.Empty())
    for showtime in allshowtimes:
        print("Showtime for this date :" + showtime.date)
        for movie in showtime.movies:
            print("Movie ID : %s" % movie)


### Initialisation du client gRPC ###
def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMovieByID --------------")
        date = showtime_pb2.Date(date="20151130")
        get_showtime_by_date(stub, date)
        print("-------------- GetListShowtime --------------")
        get_list_showtimes(stub)

    channel.close()


### Lancement du client gRPC###
if __name__ == '__main__':
    run()
