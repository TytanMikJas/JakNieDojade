from datetime import timedelta
from tabulate import tabulate
import geopy.distance

TRANSPORT_SPEED_HM_H = 40

def calculate_cost(time1, time2):
    hour1, minute1, seconds1 = map(int, time1.split(':'))
    hour2, minute2, seconds2 = map(int, time2.split(':'))

    return ((hour2 - hour1) * 60 + (minute2 - minute1) + (seconds2 - seconds1) / 60) % 1440

def calculate_heuristic(x1, y1, x2, y2):
    km_difference = geopy.distance.geodesic((x1, y1), (x2, y2)).km
    return km_difference / TRANSPORT_SPEED_HM_H * 60

def get_path(prev_edges, last_node):
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

def display_table(edges, start, end, start_time, distance, changes, elapsed_time):
    headers = ["Start Stop", "Departure Time", "End Stop", "Arrival Time", "Line"]
    print(f"From  {start} to  {end} started at: {start_time}")
    print(f"Travel time: {distance}, changes {changes}")
    print(f"it took {elapsed_time:.6} seconds to calculate the path.")
    print(tabulate(edges, headers=headers, tablefmt="grid"))

def time_str_to_timedelta(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def calculate_timedelta(curr_time_str, departure_time_str):
    curr_time = time_str_to_timedelta(curr_time_str)
    departure_time = time_str_to_timedelta(departure_time_str)

    return departure_time - curr_time

def get_direct_connection(graph_dict, lines, curr_time_str, curr_node):
    final_wait_time = timedelta(days=1)
    best_line = None
    curr_line = None
    for edge in graph_dict[curr_node]:
        if curr_line != edge.line:
            min_wait_time = timedelta(days=1)
            curr_line = edge.line
            
        if edge.line in lines:
            wait_time = calculate_timedelta(curr_time_str, edge.departure_time)
            if wait_time >= timedelta(0):
                if wait_time < min_wait_time:
                    min_wait_time = wait_time

            if min_wait_time < final_wait_time:
                final_wait_time = min_wait_time
                best_line = edge.line

    final_wait_time = final_wait_time.total_seconds() // 60

    return best_line, final_wait_time