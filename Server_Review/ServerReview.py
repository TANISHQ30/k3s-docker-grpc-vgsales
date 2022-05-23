from concurrent import futures
import time
import logging

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2

import redis
import numpy as np
import re


class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):

    def GetServerResponse(self, request, context):

        lines = 0
        user_rating = []
        game_title = []

        for message in request:

            line = message.message
            processed_line = line.strip('"').split("!")

            if processed_line[0] == "gamecomm":

                review_line = processed_line[1].strip(" ").split(",")
                # print('Review Line --> ', review_line)

                lines += 1

                user_rating.append(float(review_line[2]))
                game_title.append(review_line[0])

                if lines % 2 == 0: 
                    max_user_rating = user_rating[1]
                    max_game_title = game_title[1]
                    if(user_rating[0] > user_rating[1]):
                        max_user_rating = user_rating[0]
                        max_game_title = game_title[0]
                    
                    user_rating.clear()
                    game_title.clear()

                    # print("Max game title: ", max_game_title)
                    # print("Max rating: ", max_user_rating)

                    try:
                        conn = redis.StrictRedis(host='redis', port=6379)
                        conn.set("log.greeter_server.game_title", str(max_game_title))
                        conn.set("log.greeter_server.user_rating", str(max_user_rating))
                        
                    except Exception as ex:
                        print('Redis Error: ', ex)

        return bidirectional_pb2.Response(response=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(
        BidirectionalService(), server)
    server.add_insecure_port('[::]:50061')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()