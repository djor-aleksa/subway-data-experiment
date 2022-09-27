import pprint


class Edge:

    def __init__(self, start_station, end_station, line_number, line_color):
        self.start_station = start_station
        self.end_station = end_station
        self.line_number = line_number
        self.line_color = line_color


class Graph:

    def __init__(self, nodes: list = [], directed=True):
        self._nodes = nodes
        self.directed = directed
        self._adj_list = {node: set() for node in self._nodes}
        self._cache = {}

    @property
    def cache(self):
        return self._cache

    def add_edge(self, edge: Edge):

        if edge.start_station not in self._nodes:
            self._nodes.append(edge.start_station)

        if edge.end_station not in self._nodes:
            self._nodes.append(edge.end_station)

        if self._adj_list.get(edge.start_station, None) is None:
            self._adj_list[edge.start_station] = set()

        if self._adj_list.get(edge.end_station, None) is None:
            self._adj_list[edge.end_station] = set()

        self._adj_list[edge.start_station].add((edge.end_station, edge.line_color.capitalize()
                                                + f' No.{edge.line_number}'))

        if not self.directed:
            self._adj_list[edge.end_station].add((edge.start_station, edge.line_color.capitalize()
                                                  + f' No. {edge.line_number}'))

    def print(self):
        pprint.pprint(self._adj_list)

    def find_shortest_route(self, node_1, node_2, use_cache=True):
        cache_key = self.get_cache_key(node_1, node_2)
        if cache_key in self._cache and use_cache is True:
            return self._cache[cache_key]
        else:
            result = self._find_shortest_route(node_1, node_2)
            if use_cache is True:
                self._cache[cache_key] = self.route_str(result[0], result[1])
            return result

    def _find_shortest_route(self, node_1, node_2, label=None, path=None, labels_route=None):
        if path is None:
            path = []
            labels_route = []

        path = path + [node_1]
        labels_route = labels_route + [label]

        if node_1 == node_2:
            return path, labels_route

        shortest = None
        shortest_lines = None

        for node in self._adj_list[node_1]:
            if node[0] not in path:
                result = self._find_shortest_route(node[0], node_2, node[1], path, labels_route)
                new_path = result[0]
                new_lines = result[1]
                if new_path:
                    if not shortest or len(new_path) < len(shortest):
                        shortest = new_path
                        shortest_lines = new_lines

        return shortest, shortest_lines

    def populate_cache(self):
        for node_1 in self._nodes:
            for node_2 in self._nodes:
                cache_key = self.get_cache_key(node_1, node_2)
                if node_1 != node_2 and not self._cache.get(cache_key, None):
                    result = self._find_shortest_route(node_1, node_2)
                    self._cache[cache_key] = self.route_str(result[0], result[1])

    @staticmethod
    def route_str(route_stations: list, route_line_numbers: list):
        result = ""
        if len(route_stations) > 1 and len(route_line_numbers) > 0:
            current_line_number = None
            for i, station in enumerate(route_stations):
                if current_line_number != route_line_numbers[i - 1]:
                    result += f'--{station}--(TAKE {route_line_numbers[i - 1]})'
                    current_line_number = route_line_numbers[i - 1]
                elif i > 0 and i != len(route_stations) - 1:
                    result += f'--{station}--'
                else:
                    result += f'{station}'
        return result

    @staticmethod
    def get_cache_key(node_1, node_2):
        return "<-->".join(tuple(sorted((node_1, node_2))))
