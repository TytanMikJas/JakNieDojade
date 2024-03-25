from Graph import Graph
from LinesGraph import LinesGraph
from utils import estimate_travel_time
from algorithms import dijkstra, astar_time, astar_distance

START = 'KWISKA'
END = 'PL. GRUNWALDZKI'
TIME = '9:00:00'
HEURISTIC = estimate_travel_time

def main():
    graph_dict = Graph('updated.csv').graph_dict
    lines_dict = LinesGraph('updated.csv').graph_dict
    
    dijkstra(graph_dict, START, END, TIME)
    astar_time(graph_dict, START, END, TIME, HEURISTIC)
    astar_distance(graph_dict, lines_dict, START, END, TIME, HEURISTIC)
    
if __name__ == "__main__":
    main()