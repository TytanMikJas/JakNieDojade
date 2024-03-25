import pandas as pd
import pickle
import os
from Edge import Edge

class Graph:
    def __init__(self, path_to_csv):
        self.graph_dict = self.loadGraph(path_to_csv)

    def loadGraph(self, path_to_csv):
        graph = dict()
        
        if os.path.exists(path_to_csv + '.pkl'):
            with open(path_to_csv + '.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            data = pd.read_csv(path_to_csv)
            for _, row in data.iterrows():            
                id = int(row['id'])
                company = str(row['company'])
                line = str(row['line'])
                departure_time = str(row['departure_time'])
                arrival_time = str(row['arrival_time'])
                start_stop = str(row['start_stop']).upper()
                end_stop = str(row['end_stop']).upper()
                start_stop_lat = float(row['start_stop_lat'])
                start_stop_lon = float(row['start_stop_lon'])
                end_stop_lat = float(row['end_stop_lat'])
                end_stop_lon = float(row['end_stop_lon'])
                
                edge = Edge(id, company, line, departure_time, arrival_time, start_stop, end_stop, start_stop_lat,
                            start_stop_lon, end_stop_lat, end_stop_lon) 
            
                if start_stop not in graph:
                    graph[start_stop] = [edge]
                else:
                    graph[start_stop].append(edge)    
                
            with open(path_to_csv + '.pkl', 'wb') as f:
                pickle.dump(graph, f)
                
        return graph       