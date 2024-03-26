class Edge:
    def __init__(self, id: int, company: str, line: str, departure_time: str, arrival_time: str, start_stop: str,
                end_stop: str, start_stop_lat: float, start_stop_lon: float, end_stop_lat: float, end_stop_lon: float, weight: float):
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
        self.weight = weight

    def get_coords(self) -> tuple[float, float]:
        return self.start_stop_lat, self.start_stop_lon