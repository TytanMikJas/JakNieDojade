import pandas as pd
import pickle
import os

class LinesGraph:
    def __init__(self, path_to_csv):
        self.graph_dict = dict()

        if os.path.exists(path_to_csv + '_lines.pkl'):
            with open(path_to_csv + '_lines.pkl', 'rb') as f:
                self.graph_dict = pickle.load(f)
        else:
            data = pd.read_csv(path_to_csv)
            for _, row in data.iterrows():            
                line = str(row['line'])
                end_stop = str(row['end_stop']).upper()

                if end_stop not in self.graph_dict:
                    self.graph_dict[end_stop] = {line}
                else:
                    self.graph_dict[end_stop].add(line)
                
            with open(path_to_csv + '_lines.pkl', 'wb') as f:
                pickle.dump(self.graph_dict, f)    
