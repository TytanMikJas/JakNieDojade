from datetime import timedelta
from tabulate import tabulate
from geopy.distance import geodesic

TRANSPORT_SPEED_KM_H = 40

def calculate_cost(time1, time2):
    hour1, minute1, seconds1 = map(int, time1.split(':'))
    hour2, minute2, seconds2 = map(int, time2.split(':'))

    return ((hour2 - hour1) * 60 + (minute2 - minute1) + (seconds2 - seconds1) / 60) % 1440

def estimate_travel_time(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    distance_km = geodesic((lat1, lon1), (lat2, lon2)).km
    return distance_km / TRANSPORT_SPEED_KM_H * 60

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

def display_journey_summary(path: list, start: str, end: str, start_time: str, distance: float, changes: int, calculation_time: float):
    headers = ["Start Stop", "Departure Time", "End Stop", "Arrival Time", "Line"]
    print(f"Journey from {start} to {end} started at: {start_time}:")
    print(f"Distance: {distance} km, Changes: {changes}")
    print(f"Calculated in {calculation_time:.4f} seconds.")
    print(tabulate(path, headers=headers, tablefmt="grid"))

def parse_time_to_timedelta(time_str: str) -> timedelta:
    h, m, s = map(int, time_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

def calculate_waiting_time(current_time_str: str, departure_time_str: str) -> timedelta:
    current_time = parse_time_to_timedelta(current_time_str)
    departure_time = parse_time_to_timedelta(departure_time_str)
    return departure_time - current_time

def find_earliest_connection(graph: dict, lines: set, current_time: str, current_node: str):
    min_wait_time = timedelta(days=1)
    best_line = None
    for edge in graph[current_node]:
        if edge.line in lines:
            wait_time = calculate_waiting_time(current_time, edge.departure_time)
            if wait_time >= timedelta(0) and wait_time < min_wait_time:
                min_wait_time = wait_time
                best_line = edge.line

    wait_minutes = min_wait_time.total_seconds() / 60
    return best_line, wait_minutes