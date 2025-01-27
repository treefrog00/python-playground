from fit_data import load_fit_file
import csv
from lat_lon_code import lat_lon_distance
import gzip
import io
import fitdecode
from data_folders import original_activities_folder, data_folder

SMALL_CHUNK_SIZE = 2


def find_back_at_start(fit_data):
    for record in fit_data.records:
        if record.has_field("position_lat") and record.has_field("position_long"):

            start = {
                "lat": record.get_value("position_lat") / ((2**32) / 360),
                "lon": record.get_value("position_long") / ((2**32) / 360),
            }

            break

    for i, record in enumerate(fit_data.records):
        if i < 40:
            continue
        if record.has_field("position_lat") and record.has_field("position_long"):

            lat_lon = {
                "lat": record.get_value("position_lat") / ((2**32) / 360),
                "lon": record.get_value("position_long") / ((2**32) / 360),
            }

            distance = lat_lon_distance(
                start["lat"], start["lon"], lat_lon["lat"], lat_lon["lon"]
            )
            if distance < 0.01:
                print(f"back at start within {distance}km by {i}, {distance:.2f}km")
                return i


def crop_file(fit_path, end_index):
    with gzip.open(fit_path, "rb") as gz_file:
        binary_data = io.BytesIO(gz_file.read())

    output_data = io.BytesIO()
    all_data = bytearray()

    with fitdecode.FitReader(binary_data, processor=None, keep_raw_chunks=True) as fit:
        record_count = 0
        for frame in fit:
            # Always write header and definition frames
            if frame.frame_type in (
                fitdecode.FIT_FRAME_HEADER,
                fitdecode.FIT_FRAME_DEFINITION,
            ):
                chunk = frame.chunk.bytes
                output_data.write(chunk)
                all_data.extend(chunk)
            # For data frames, only write if before end_index
            elif frame.frame_type == fitdecode.FIT_FRAME_DATA:
                if frame.name == "record":
                    if record_count >= end_index:
                        continue
                    record_count += 1
                chunk = frame.chunk.bytes
                output_data.write(chunk)
                all_data.extend(chunk)
            # Skip original CRC frame as we'll calculate our own

    # Write the new CRC
    crc = fitdecode.utils.compute_crc(all_data)
    output_data.write(crc.to_bytes(2, byteorder="little"))

    # Write the output
    stem = fit_path.stem
    dir = data_folder / "strava_cropped"
    dir.mkdir(exist_ok=True)
    (dir / f"{stem}").write_bytes(output_data.getvalue())


def write_uncompressed_copy(fit_path):
    with gzip.open(fit_path, "rb") as gz_file:
        binary_data = io.BytesIO(gz_file.read())
        stem = fit_path.stem
        dir = data_folder / "strava_uncompressed"
        dir.mkdir(exist_ok=True)
        (dir / f"{stem}").write_bytes(binary_data.read())


def process_suspicious_activities():
    csv_path = data_folder / "suspicious_activities_fit_original.csv"

    with csv_path.open("r") as f:
        reader = csv.reader(f)
        for row in reader:
            filename = row[0]
            fit_path = original_activities_folder / filename
            fit_data = load_fit_file(fit_path)
            write_uncompressed_copy(fit_path)
            sport = fit_data.session_metadata["sport"]
            print(fit_path)
            print(sport)
            end_index = find_back_at_start(fit_data)
            # if not end_index:
            #     print("Couldn't find back at start")
            #     end_index = ???(fit_data)
            #
            if end_index:
                crop_file(fit_path, end_index)
            print("\n\n")


if __name__ == "__main__":
    process_suspicious_activities()
