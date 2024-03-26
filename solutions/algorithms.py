import time
import math
import heapq
from distance_calculations import calculate_cost, find_earliest_connection

LINE_CHANGE_COST = 15

def dijkstra(graph_dict: dict, start: str, end: str, start_time: str):
    start_exec_time = time.time()
    
    distances = {node: float('inf') for node in graph_dict}
    prev_edges = {node: None for node in graph_dict}
    
    distances[start] = 0
    pq = [(0, start, start_time)]
    
    last_node = None

    while pq:
        curr_dist, curr_node, curr_time = heapq.heappop(pq)
            
        if curr_node == end:
            last_node = curr_node
            break
        
        if curr_dist > distances[curr_node]:
            continue
        
        for edge in graph_dict[curr_node]:
            waiting_time= calculate_cost(curr_time, edge.departure_time)
            travel_time = calculate_cost(edge.departure_time, edge.arrival_time)
            new_distance = curr_dist + travel_time + waiting_time

            if new_distance < distances[edge.end_stop]:
                distances[edge.end_stop] = new_distance
                prev_edges[edge.end_stop] = [edge.start_stop, edge.departure_time, edge.end_stop, edge.arrival_time, edge.line]
                heapq.heappush(pq, (new_distance, edge.end_stop, edge.arrival_time))
    
    elapsed_time = time.time() - start_exec_time
    
    return distances, prev_edges, last_node, start, end, start_time, elapsed_time


def astar_time(graph_dict: dict, start: str, end: str, start_time: str, heuristic):
    final_stop_lat, final_stop_lon = graph_dict[end][0].get_coords()
    
    start_exec_time = time.time()
        
    distances = {node: float('inf') for node in graph_dict}
    prev_edges = {node: None for node in graph_dict}
    
    distances[start] = 0
    pq = [(0, start, start_time, 0)]
    
    last_node = None
    
    while pq:
        _, curr_node, curr_time, g_dist = heapq.heappop(pq)
        
        if curr_node == end:
            last_node = curr_node
            break
        
        if g_dist > distances[curr_node]:
            continue

        for edge in graph_dict[curr_node]:
            waiting_time = calculate_cost(curr_time, edge.departure_time)
            travel_time = calculate_cost(edge.departure_time, edge.arrival_time)
            new_distance = distances[curr_node] + travel_time + waiting_time
            
            if new_distance < distances[edge.end_stop]:
                distances[edge.end_stop] = new_distance
                prev_edges[edge.end_stop] = [edge.start_stop, edge.departure_time, edge.end_stop, edge.arrival_time, edge.line]
                priority = new_distance + heuristic(edge.end_stop_lat, edge.end_stop_lon, final_stop_lat, final_stop_lon)
                heapq.heappush(pq, (priority, edge.end_stop, edge.arrival_time, new_distance))
    
    elapsed_time = time.time() - start_exec_time
    
    return distances, prev_edges, last_node, start, end, start_time, elapsed_time


def astar_stops(graph_dict: dict, lines_dict: dict, start: str, end: str, start_time: str, heuristic):
    final_stop_lat, final_stop_lon = graph_dict[end][0].get_coords()
    
    start_exec_time = time.time()
        
    distances = {node: float('inf') for node in graph_dict}
    prev_edges = {node: None for node in graph_dict}
    
    distances[start] = 0
    pq = [(0, start, start_time, 0)]
    
    last_node = None
    direct_line = None
    
    while pq:
        _, curr_node, curr_time, g_dist = heapq.heappop(pq)
        
        if curr_node == end:
            last_node = curr_node
            break
        
        if g_dist > distances[curr_node]:
            continue
        
        prev_line = prev_edges[curr_node][4] if prev_edges[curr_node] else ''

        for edge in graph_dict[curr_node]:
            
            line_change_penalty = LINE_CHANGE_COST if (prev_line and prev_line != edge.line) else 0
            
            if direct_line and edge.line != direct_line:
                continue
            
            if not direct_line and edge.line in lines_dict[end]:
                direct_line, best_time = find_earliest_connection(graph_dict, lines_dict[end], curr_time, curr_node)
                if best_time > LINE_CHANGE_COST:
                    direct_line = None
                if edge.line != direct_line:
                    continue
            
            waiting_time = calculate_cost(curr_time, edge.departure_time)
            travel_time = calculate_cost(edge.departure_time, edge.arrival_time)
            new_distance = distances[curr_node] + travel_time + waiting_time
            
            if new_distance + line_change_penalty < distances[edge.end_stop]:
                distances[edge.end_stop] = new_distance
                prev_edges[edge.end_stop] = [edge.start_stop, edge.departure_time, edge.end_stop, edge.arrival_time, edge.line]
                priority = new_distance + heuristic(edge.end_stop_lat, edge.end_stop_lon, final_stop_lat, final_stop_lon) + line_change_penalty
                heapq.heappush(pq, (priority, edge.end_stop, edge.arrival_time, new_distance))
    
    elapsed_time = time.time() - start_exec_time
    
    return distances, prev_edges, last_node, start, end, start_time, elapsed_time


def tabu_search(stops, trip_start_time, graph_dict, heuristric):
    start_exec_time = time.time()
    n_stops = len(stops)
    max_iterations = math.ceil(1.1*(n_stops**2))
    turns_improved = 0
    improve_thresh = 2*math.floor(math.sqrt(max_iterations))
    tabu_list = []
    tabu_tenure = n_stops

    distances = [[astar_time(graph_dict, start, stop, trip_start_time, heuristric)[0][stop] for start in stops] for stop in stops]

    total = 0
    for i in range(n_stops):
            for j in range(n_stops):
                total += distances[i][j]

    aspiration_criteria = (total/(n_stops**2))*2.2
    current_solution = list(range(n_stops))
    best_solution = current_solution[:]
    best_solution_cost = sum([distances[current_solution[i]][current_solution[(i+1)%n_stops]] for i in range(n_stops)])

    for iteration in range(max_iterations):
        if turns_improved>improve_thresh:
            break
        best_neighbor = None
        best_neighbor_cost = float('inf')
        tabu_candidate = (0,0)
        for i in range(n_stops):
            for j in range(i+1, n_stops):
                neighbor = current_solution[:]
                if i > 0:
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbor_cost = sum([distances[neighbor[i]][neighbor[(i+1)%n_stops]] for i in range(n_stops)])
                if (i,j) not in tabu_list or neighbor_cost < aspiration_criteria:
                    if neighbor_cost < best_neighbor_cost:
                        best_neighbor = neighbor[:]
                        best_neighbor_cost = neighbor_cost
                        tabu_candidate = (i,j)
        if best_neighbor is not None:
            current_solution = best_neighbor[:]
            tabu_list.append(tabu_candidate)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            if best_neighbor_cost < best_solution_cost:
                best_solution = best_neighbor[:]
                best_solution_cost = best_neighbor_cost
                turns_improved=0
            else:
                turns_improved=turns_improved+1

        print("Iteration {}: Best solution cost = {}".format(iteration, best_solution_cost))

    elapsed_time = time.time()
    print(f"time: {elapsed_time - start_exec_time}")
    stops_sorted = [stops[i] for i in best_solution]
    
    print(f"Best solution: {stops_sorted}")