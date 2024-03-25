from Graph import Graph
from algorithms import dijkstra, astar_time, astar_distance
from utils import calculate_heuristic
from LinesGraph import LinesGraph

START = 'KWISKA'
END = 'PL. GRUNWALDZKI'
TIME = '9:00:00'
HEURISTIC = calculate_heuristic

def main():
    graph_dict = Graph('updated.csv').graph_dict
    lines_dict = LinesGraph('updated.csv').graph_dict
    dijkstra(graph_dict, START, END, TIME)
    astar_time(graph_dict, START, END, TIME, heuristic=HEURISTIC)
    astar_distance(graph_dict, lines_dict, START, END, TIME, heuristic=HEURISTIC)
    
if __name__ == "__main__":
    main()