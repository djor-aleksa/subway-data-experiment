import time
import random
from graph import *
import csv

if __name__ == "__main__":

    NUMBER_OF_RANDOM_CONNECTIONS = 10_000
    vienna_subway_graph = Graph(directed=False)

    print('Populating graph from .csv file as a adjacency list...')
    # Loading the data from .cvs file and creating a graph
    with open('vienna_subway.csv') as csv_file:
        csv_reader = csv.reader(csv_file.readlines()[1:], delimiter=';')
        stations = set()
        for row in csv_reader:
            stations.add(row[0])
            stations.add(row[1])
            vienna_subway_graph.add_edge(Edge(row[0], row[1], row[2], row[3]))

    print("Graph populated.\n")

    # Step 1 - Generate 10000 random start and end stations and finding the shortest path between them without caching
    # the results
    print(f'''Generating random start and end stations and finding the shortest path between 
    them without caching {NUMBER_OF_RANDOM_CONNECTIONS} times...''')
    start_time = time.time()

    for _ in range(0, NUMBER_OF_RANDOM_CONNECTIONS):
        random_station_1, random_station_2 = tuple(random.choices(list(stations), k=2))
        vienna_subway_graph.find_shortest_route(random_station_1, random_station_2, use_cache=False)

    print(f'Time needed to complete all operations: {round((time.time() - start_time) * 1000)} milliseconds.')
    print(f'''Avg. Time per operation: {round((time.time() - start_time) * 1000) / NUMBER_OF_RANDOM_CONNECTIONS}
           milliseconds.\n''')

    # Step 2 - Populating in-memory cache
    print("Populating cache...")
    start_populating_cache = time.time()

    vienna_subway_graph.populate_cache()

    print(f'Completed populating cache in {round((time.time() - start_populating_cache) * 1000)} milliseconds.\n')

    # Step 3 - Repeat Step 1 with cache
    start_time = time.time()

    print(f'''Generating random start and end stations and finding the shortest path between 
          them with caching {NUMBER_OF_RANDOM_CONNECTIONS} times...''')

    for _ in range(0, NUMBER_OF_RANDOM_CONNECTIONS):
        random_station_1, random_station_2 = tuple(random.choices(list(stations), k=2))
        vienna_subway_graph.find_shortest_route(random_station_1, random_station_2, use_cache=True)

    print(f"Time needed to complete all operations: {round((time.time() - start_time) * 1000)} milliseconds")
    print(f"Avg time: {round((time.time() - start_time) * 1000) / NUMBER_OF_RANDOM_CONNECTIONS} milliseconds")





