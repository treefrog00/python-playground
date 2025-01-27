from dataclasses import dataclass

suspicious_speeds = {"hiking": 10, "running": 20, "cycling": 60}


@dataclass
class Activity:
    file: str
    sport: str
    distance: float
    max_chunk_speed: float
    chunk_speeds: list[float]
