class Edge:
    def __init__(self, id, company, line, departure_time, arrival_time, start_stop,
                end_stop, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon):
        self.id = id
        self.company = company
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.start_stop_lat = start_stop_lat
        self.start_stop_lon = start_stop_lon
        self.end_stop_lat = end_stop_lat
        self.end_stop_lon = end_stop_lon
    
    def get_coords(self):
        return self.start_stop_lat, self.start_stop_lon

    def __str__(self) -> str:
        return (
            f'Line: {self.line} | '
            f'Start Node: {self.startNode} | '
            f'Departure Time: {self.departureTime} | '
            f'Arrival Time: {self.arrivalTime} | '
            f'End Node: {self.endNode} | \n'
        )
