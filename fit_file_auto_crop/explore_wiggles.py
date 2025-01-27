from fit_data import load_fit_file
import csv
from wiggles_finder import munge_wiggles_data

from data_folders import original_activities_folder, data_folder


def export_wiggles(stem, wiggles):
    export_df = wiggles.select(["start_lat", "start_lon", "lat", "lon", "speed_kmh"])

    output_file = data_folder / "wiggles_json" / f"wiggles_{stem}.json"
    export_df.write_json(output_file)


def process_suspicious_activities():
    csv_path = data_folder / "suspicious_activities_fit_original.csv"

    with csv_path.open("r") as f:
        reader = csv.reader(f)
        for row in reader:
            filename = row[0]
            fit_path = original_activities_folder / filename
            fit_data = load_fit_file(fit_path)
            wiggles = munge_wiggles_data(fit_data)
            stem = fit_path.stem.split(".")[0]
            export_wiggles(stem, wiggles)


if __name__ == "__main__":
    process_suspicious_activities()
