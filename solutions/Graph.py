import pandas as pd
import pickle
from distance_calculations import calculate_cost
from typing import Dict
from Edge import Edge

class Graph:
    def __init__(self, path_to_csv: str):
        self.graph_dict = self.load_graph(path_to_csv)

    def load_graph(self, path_to_csv: str) -> Dict[str, list[Edge]]:
        pickle_path = f'{path_to_csv}.pkl'
        try:
            with open(pickle_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return self.load_from_csv(path_to_csv, pickle_path)

    def load_from_csv(self, path_to_csv: str, pickle_path: str) -> Dict[str, list[Edge]]:
        data = pd.read_csv(path_to_csv)
        graph = dict()
        for _, row in data.iterrows():
            edge = Edge(
                id=int(row['id']),
                company=str(row['company']),
                line=str(row['line']),
                departure_time=str(row['departure_time']),
                arrival_time=str(row['arrival_time']),
                start_stop=str(row['start_stop']).upper(),
                end_stop=str(row['end_stop']).upper(),
                start_stop_lat=float(row['start_stop_lat']),
                start_stop_lon=float(row['start_stop_lon']),
                end_stop_lat=float(row['end_stop_lat']),
                end_stop_lon=float(row['end_stop_lon']),
                weight =float(calculate_cost(str(row['departure_time']), str(row['arrival_time'])))
            )
            if edge.start_stop not in graph:
                graph[edge.start_stop] = [edge]
            else:
                graph[edge.start_stop].append(edge)
        
        with open(pickle_path, 'wb') as f:
            pickle.dump(graph, f)
        
        return graph
