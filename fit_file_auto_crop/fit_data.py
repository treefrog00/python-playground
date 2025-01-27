import gzip
import io
import fitdecode
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FitData:
    records: List[Any]
    file_metadata: Dict[str, Any]
    activity_metadata: Dict[str, Any]
    session_metadata: Dict[str, Any]


def load_fit_file(file_path):
    records = []
    file_metadata = {}
    activity_metadata = {}
    session_metadata = {}

    with gzip.open(file_path, "rb") as gz_file:
        fit_data = io.BytesIO(gz_file.read())
        # skip CRC check for a minor performance boost
        with fitdecode.FitReader(
            fit_data, check_crc=fitdecode.CrcCheck.DISABLED
        ) as fit:
            for frame in fit:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "record":
                        records.append(frame)
                    elif frame.name == "file_id":
                        file_metadata = {
                            field.name: field.value for field in frame.fields
                        }
                    elif frame.name == "activity":
                        activity_metadata = {
                            field.name: field.value for field in frame.fields
                        }
                    elif frame.name == "session":
                        session_metadata = {
                            field.name: field.value for field in frame.fields
                        }
    return FitData(
        records=records,
        file_metadata=file_metadata,
        activity_metadata=activity_metadata,
        session_metadata=session_metadata,
    )


def calculate_chunk_speeds(fit_data, chunk_size):
    # Get all data records that contain position and timestamp data
    data = []
    for record in fit_data.records:
        if record.has_field("timestamp") and record.has_field("distance"):

            data.append(
                {
                    "distance": record.get_value("distance"),
                    "timestamp": record.get_value("timestamp"),
                }
            )

    chunk_speeds = []
    for i in range(0, len(data), chunk_size):
        end_index = min(len(data) - 1, i + chunk_size - 1)

        if i == end_index:  # Need at least 2 points to calculate speed
            continue

        # Calculate total distance and time for chunk
        total_distance = data[end_index]["distance"] - data[i]["distance"]
        time_diff = (
            data[end_index]["timestamp"] - data[i]["timestamp"]
        ).total_seconds() / 3600  # Convert to hours

        if time_diff > 0:
            speed = total_distance / time_diff  # km/h
            chunk_speeds.append(speed / 1000)

    return chunk_speeds if chunk_speeds else [0]
