from concurrent import futures

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import time
import redis
import numpy as np
import json

class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):

    def __init__(self):
        self.msg = ["Highest_selling_game", "Average_sell_of_games",
                    "Highest_selling_genre", "Lowest_selling_genre"]
        self.row_index = 0
        
    def GetServerResponse(self, request, context):
        index = 1
        previous_total = 0
        previous_genre = ''
        previous_game_name = ''
        start_time = time.time()
        genre = ''
        line_count = 0
        total = 0
        cumulative_avg_res = {}
        genre_dict = {}
        for messages in request:
            line = messages.message
            total_game_sell, top_genre, high_selling_game, start_time, genre_dict, line_count = getAnalysis(line, total, index, previous_total, 
                previous_genre, previous_game_name, genre, genre_dict, start_time, line_count)
            if index % 2 == 0:
                average = total_game_sell / 8
                previous_total = 0
                previous_genre = ''
                previous_game_name = ''
                genre = ''
                total = 0
                current_time = time.time()
                try:
                    msg1 = round(float(total_game_sell), 3)
                    msg2 = round(float(average), 3)
                    conn = redis.StrictRedis(host='redis',port=6379)
                    conn.set("log.greeter_server.msg1", str(total_game_sell))
                    conn.set("log.greeter_server.msg2", str(msg2))
                    conn.set("log.greeter_server.msg3", str(top_genre))
                    conn.set("log.greeter_server.msg4", str(high_selling_game))
                    conn.set("secondsPassed", str(int(current_time - start_time)))

                    #'line_count' is incremented by 1 after a second
                    if line_count>=180:
                        cumulative_avg_res = genre_dict
                        conn.set("metrics", json.dumps(cumulative_avg_res))
                        genre_dict.clear()
                        line_count = 0
                    
                    if current_time - start_time >= 180:
                        start_time = time.time()

                except Exception as ex:
                    print("Redis Error: ",ex)

            index+=1
            print(bidirectional_pb2.Response(response = True))
        return bidirectional_pb2.Response(response = True)

def getAnalysis(line, total, index, previous_total, previous_genre, high_selling_game, genre, genre_dict, start_time, line_count):
    
    processed_line = line.strip('"').split(",")
    line_count+=1

    for i in range(6,10):
        total += float(processed_line[i])
        total = round(total, 3)
    genre = processed_line[4]

    if genre not in genre_dict.keys():
        genre_dict[genre] = 0
    genre_dict[genre] += total / 4

    if(index %2 != 0):
        previous_total = total
        previous_genre = genre
        high_selling_game = processed_line[1]
    else:
        if previous_total > total:
            return previous_total, previous_genre, high_selling_game, start_time, genre_dict, line_count

    return total, genre, processed_line[1], start_time, genre_dict, line_count

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(BidirectionalService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()       

if __name__ == '__main__':
    serve()
