import time
import heapq
from utils import calculate_cost, reconstruct_path, display_journey_summary, find_earliest_connection

LINE_CHANGE_COST = 20

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
    
    final_list, changes = reconstruct_path(prev_edges, last_node)

    display_journey_summary(final_list, start, end, start_time, distances[end], changes, elapsed_time)


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
    
    final_list, changes = reconstruct_path(prev_edges, last_node)
    
    display_journey_summary(final_list, start, end, start_time, distances[end], changes, elapsed_time)


def astar_distance(graph_dict: dict, lines_dict: dict, start: str, end: str, start_time: str, heuristic):
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
    
    final_list, changes = reconstruct_path(prev_edges, last_node)
    
    display_journey_summary(final_list, start, end, start_time, distances[end], changes, elapsed_time)
    