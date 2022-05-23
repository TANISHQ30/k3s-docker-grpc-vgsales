from __future__ import print_function

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import random
import time

def generate_messages():
    f = open("Client/vgsales.csv", "r")
    index = 0
    for line in f:
        # print(line)
        # print(type(line))
        if index != 0:
            msg = bidirectional_pb2.Message(message=line)
            yield msg
        if index % 2 == 0:
            time.sleep(1)
        index = index + 1

def run():
    with grpc.insecure_channel('server:50051') as channel:
        stub = bidirectional_pb2_grpc.BidirectionalStub(channel)
        response = stub.GetServerResponse(generate_messages())
        print("There server has completed =  %s" % response.response)

if __name__ == '__main__':
    run()