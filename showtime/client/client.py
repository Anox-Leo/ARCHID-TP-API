import grpc

import showtime_pb2
import showtime_pb2_grpc


def get_showtime_by_date(stub,date):
    showtime = stub.GetShowtimeByDate(date)
    print(showtime)

def get_list_movies(stub):
    allshowtimes = stub.GetShowtimes(showtime_pb2.Empty())
    for showtime in allshowtimes:
        print("Movies for this date :" + showtime.date)
        for movie in showtime.movies:
            print("\s" + movie)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMovieByID --------------")
        date = showtime_pb2.Date(date="20151130")
        get_showtime_by_date(stub, date)
        print("-------------- GetListMovies --------------")
        get_list_movies(stub)

    channel.close()

if __name__ == '__main__':
    run()
