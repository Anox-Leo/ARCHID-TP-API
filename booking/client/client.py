import grpc

import booking_pb2
import booking_pb2_grpc


def get_booking_by_user_id(stub,id):
    booking = stub.GetBookingByUserId(id)
    print(booking)

def get_list_bookings(stub):
    allbookings = stub.GetBookings(booking_pb2.Empty())
    for booking in allbookings:
        print("Bookings for user " + booking.id + " :" + "\n" + "Date : " +
        booking.date + "\n" + "Movies ID : " + str(booking.movies) + "\n")


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3004') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetBookingsByUserId --------------")
        userid = booking_pb2.UserId(id="chris_rivers")
        get_booking_by_user_id(stub, userid)
        print("-------------- GetListBooking --------------")
        get_list_bookings(stub)

    channel.close()

if __name__ == '__main__':
    run()