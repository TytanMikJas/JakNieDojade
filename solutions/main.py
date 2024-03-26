from Graph import Graph
from LinesGraph import LinesGraph
from display_solutions import display_solution
from distance_calculations import estimate_travel_time
from algorithms import dijkstra, astar_time, astar_stops, tabu_search

START = 'KWISKA'
END = 'PL. GRUNWALDZKI'
TIME = '9:00:00'
HEURISTIC = estimate_travel_time

def main():
    graph_dict = Graph('updated.csv').graph_dict
    lines_dict = LinesGraph('updated.csv').graph_dict

    display_solution(dijkstra(graph_dict, START, END, TIME))
    display_solution(astar_time(graph_dict, START, END, TIME, HEURISTIC))
    display_solution(astar_stops(graph_dict, lines_dict, START, END, TIME, HEURISTIC))

    stops = ["POMORSKA", "PL. GRUNWALDZKI", "DUBOIS", "MOSTY POMORSKIE", "ŚWIDNICKA"]
    
    tabu_search(stops, TIME, graph_dict, HEURISTIC)
    
if __name__ == "__main__":
    main()