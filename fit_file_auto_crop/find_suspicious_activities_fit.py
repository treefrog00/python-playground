from typing import Iterable
from collections import defaultdict
from suspicious_activities import suspicious_speeds, Activity
from data_folders import original_activities_folder, data_folder
import csv
from fit_data import load_fit_file, calculate_chunk_speeds

LARGE_CHUNK_SIZE = 100


def activities_sorted_by_max_chunk_speed(activities):
    activities_by_sport = defaultdict(list)
    for activity in activities:
        activities_by_sport[activity.sport].append(activity)

    for sport, sport_activities in activities_by_sport.items():
        print(sport)
        for activity in sorted(
            sport_activities, key=lambda a: a.max_chunk_speed, reverse=True
        ):
            print(activity)


def get_suspicious_activities(activities) -> Iterable[Activity]:
    for activity in activities:
        if activity.max_chunk_speed > suspicious_speeds[activity.sport]:
            yield activity


def explore_folder(folder):
    activities = []

    for file_path in folder.glob("*.fit.gz"):
        fit_data = load_fit_file(file_path)
        sport = fit_data.session_metadata["sport"]
        if sport not in ["cycling", "running", "hiking"]:
            continue

        chunk_speeds = calculate_chunk_speeds(fit_data, LARGE_CHUNK_SIZE)
        max_chunk_speed = max(chunk_speeds) if chunk_speeds else 0.0

        if max_chunk_speed < suspicious_speeds[sport]:
            continue

        activities.append(
            Activity(
                file=file_path.name,
                sport=sport,
                distance=fit_data.session_metadata["total_distance"] / 1000,
                max_chunk_speed=max_chunk_speed,
                chunk_speeds=chunk_speeds,
            )
        )
        if len(activities) % 20 == 0:
            print(len(activities))

    candidates_for_crop = list(get_suspicious_activities(activities))

    with open(data_folder / "suspicious_activities_fit.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for file in sorted(x.file for x in candidates_for_crop):
            writer.writerow([file])


def run():
    explore_folder(original_activities_folder)


if __name__ == "__main__":
    run()
