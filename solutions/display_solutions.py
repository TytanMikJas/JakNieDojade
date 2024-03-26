from tabulate import tabulate

def reconstruct_path(prev_edges: dict, last_node: str):
    final_list = []
    
    changes = 0
    prev_line = prev_edges[last_node][4]
        
    while last_node in prev_edges and prev_edges[last_node]:
        row = prev_edges[last_node]
        if row[4] != prev_line: 
            changes += 1
            prev_line = row[4]
        
        final_list.append(row)
        last_node = row[0] if row[0] in prev_edges else None

    final_list.reverse()
    
    return final_list, changes

def display_journey_summary(path: list, start: str, end: str, start_time: str, time: float, changes: int, calculation_time: float):
    headers = ["Start Stop", "Departure Time", "End Stop", "Arrival Time", "Line"]
    print(f"Journey from {start} to {end} started at: {start_time}:")
    print(f"Travel time: {time} minutes")
    print(f"Number of changes: {changes}")
    print(f"Elapsed in: {calculation_time:.4f} seconds")
    print(tabulate(path, headers=headers, tablefmt="grid"))

def display_solution(data):
    distances, prev_edges, last_node, start, end, start_time, elapsed_time = data
    final_list, changes = reconstruct_path(prev_edges, last_node)
    display_journey_summary(final_list, start, end, start_time, distances[end], changes, elapsed_time)
