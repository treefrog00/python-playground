from pathlib import Path
import os

# Use the environment variable if set, otherwise use a default path
data_folder = Path(os.getenv("DATA_FOLDER"))

original_activities_folder = data_folder / "strava_export_orig" / "activities"
edited_activities_folder = data_folder / "strava_export_edited" / "activities"
