# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import booking_pb2 as booking__pb2


class BookingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBookingByUserId = channel.unary_unary(
                '/Booking/GetBookingByUserId',
                request_serializer=booking__pb2.UserId.SerializeToString,
                response_deserializer=booking__pb2.BookingData.FromString,
                )
        self.GetBookings = channel.unary_stream(
                '/Booking/GetBookings',
                request_serializer=booking__pb2.Empty.SerializeToString,
                response_deserializer=booking__pb2.BookingData.FromString,
                )


class BookingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetBookingByUserId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBookings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBookingByUserId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBookingByUserId,
                    request_deserializer=booking__pb2.UserId.FromString,
                    response_serializer=booking__pb2.BookingData.SerializeToString,
            ),
            'GetBookings': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBookings,
                    request_deserializer=booking__pb2.Empty.FromString,
                    response_serializer=booking__pb2.BookingData.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Booking', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Booking(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetBookingByUserId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Booking/GetBookingByUserId',
            booking__pb2.UserId.SerializeToString,
            booking__pb2.BookingData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBookings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Booking/GetBookings',
            booking__pb2.Empty.SerializeToString,
            booking__pb2.BookingData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)