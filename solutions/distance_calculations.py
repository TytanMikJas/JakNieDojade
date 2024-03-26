from datetime import timedelta
from geopy.distance import geodesic

TRANSPORT_SPEED_KM_H = 40

def calculate_cost(time1: str, time2: str):
    hour1, minute1, seconds1 = map(int, time1.split(':'))
    hour2, minute2, seconds2 = map(int, time2.split(':'))

    return ((hour2 - hour1) * 60 + (minute2 - minute1) + (seconds2 - seconds1) / 60) % 1440

def estimate_travel_time(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    distance_km = geodesic((lat1, lon1), (lat2, lon2)).km
    return distance_km / TRANSPORT_SPEED_KM_H * 60

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