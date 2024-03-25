import time
import heapq
from utils import calculate_cost, get_path, display_table, get_direct_connection

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
            new_distance = curr_dist + calculate_cost(edge.departure_time, edge.arrival_time) + calculate_cost(curr_time, edge.departure_time)

            if new_distance < distances[edge.end_stop]:
                distances[edge.end_stop] = new_distance
                prev_edges[edge.end_stop] = [edge.start_stop, edge.departure_time, edge.end_stop, edge.arrival_time, edge.line]
                heapq.heappush(pq, (new_distance, edge.end_stop, edge.arrival_time))
    
    elapsed_time = time.time() - start_exec_time
    final_list, changes = get_path(prev_edges, last_node)

    display_table(final_list, start, end, start_time, distances[end], changes, elapsed_time)


def astar_time(graph_dict: dict, start: str, end: str, start_time: str, heuristic):
    final_stop_lat, final_stop_lon = graph_dict[end][0].get_coords()
    
    start_exec_time = time.time()
        
    g_distances = {node: float('inf') for node in graph_dict}
    prev_edges = {node: None for node in graph_dict}
    
    g_distances[start] = 0
    pq = [(0, start, start_time, 0)]
    
    last_node = None
    
    while pq:
        _, curr_node, curr_time, g_dist = heapq.heappop(pq)
        
        if curr_node == end:
            last_node = curr_node
            break
        
        if g_dist > g_distances[curr_node]:
            continue

        for edge in graph_dict[curr_node]:
            new_g_distance = g_distances[curr_node] + calculate_cost(edge.departure_time, edge.arrival_time)  + calculate_cost(curr_time, edge.departure_time)
            
            if new_g_distance < g_distances[edge.end_stop]:
                g_distances[edge.end_stop] = new_g_distance
                prev_edges[edge.end_stop] = [edge.start_stop, edge.departure_time, edge.end_stop, edge.arrival_time, edge.line]
                priority = new_g_distance + heuristic(edge.end_stop_lat, edge.end_stop_lon, final_stop_lat, final_stop_lon)
                heapq.heappush(pq, (priority, edge.end_stop, edge.arrival_time, new_g_distance))
    
    elapsed_time = time.time() - start_exec_time
    final_list, changes = get_path(prev_edges, last_node)
    
    display_table(final_list, start, end, start_time, g_distances[end], changes, elapsed_time)


def astar_distance(graph_dict: dict, lines_dict: dict, start: str, end: str, start_time: str, heuristic):
    final_stop_lat, final_stop_lon = graph_dict[end][0].get_coords()
    
    start_exec_time = time.time()
        
    g_distances = {node: float('inf') for node in graph_dict}
    prev_edges = {node: None for node in graph_dict}
    
    g_distances[start] = 0
    pq = [(0, start, start_time, 0)]
    
    last_node = None
    direct_line = None
    
    while pq:
        _, curr_node, curr_time, g_dist = heapq.heappop(pq)
        
        if curr_node == end:
            last_node = curr_node
            break
        
        if g_dist > g_distances[curr_node]:
            continue
        
        prev_line = ''
        if prev_edges[curr_node]:
            prev_line = prev_edges[curr_node][4]

        for edge in graph_dict[curr_node]:
            
            if direct_line:
                if edge.line != direct_line:
                    continue
            elif edge.line in lines_dict[end]:
                direct_line, best_time = get_direct_connection(graph_dict, lines_dict[end], curr_time, curr_node)
                if best_time > LINE_CHANGE_COST:
                    direct_line = None
                if edge.line != direct_line:
                    continue
                
            if prev_line == edge.line or prev_line == '': 
                line_change_penalty = 0
            else: 
                line_change_penalty = LINE_CHANGE_COST 
            
            new_g_distance = g_distances[curr_node] + calculate_cost(edge.departure_time, edge.arrival_time)  + calculate_cost(curr_time, edge.departure_time)
            
            if new_g_distance + line_change_penalty < g_distances[edge.end_stop]:
                g_distances[edge.end_stop] = new_g_distance
                prev_edges[edge.end_stop] = [edge.start_stop, edge.departure_time, edge.end_stop, edge.arrival_time, edge.line]
                priority = new_g_distance + heuristic(edge.end_stop_lat, edge.end_stop_lon, final_stop_lat, final_stop_lon) + line_change_penalty
                heapq.heappush(pq, (priority, edge.end_stop, edge.arrival_time, new_g_distance))
    
    elapsed_time = time.time() - start_exec_time
    final_list, changes = get_path(prev_edges, last_node)
    
    display_table(final_list, start, end, start_time, g_distances[end], changes, elapsed_time)
    