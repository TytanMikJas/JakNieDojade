import pandas as pd
import pickle
from typing import Dict, Set

class LinesGraph:
    def __init__(self, path_to_csv: str):
        self.graph_dict = self.load_graph(path_to_csv)

    def load_graph(self, path_to_csv: str) -> Dict[str, Set[str]]:
        pickle_path = f'{path_to_csv}_lines.pkl'
        try:
            with open(pickle_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return self.load_from_csv(path_to_csv, pickle_path)

    def load_from_csv(self, path_to_csv: str, pickle_path: str) -> Dict[str, Set[str]]:
        data = pd.read_csv(path_to_csv)
        graph = {}
        for _, row in data.iterrows():
            line = str(row['line'])
            end_stop = str(row['end_stop']).upper()
            
            if end_stop not in graph:
                graph[end_stop] = {line}
            else:
                graph[end_stop].add(line)

        with open(pickle_path, 'wb') as f:
            pickle.dump(graph, f)

        return graph
