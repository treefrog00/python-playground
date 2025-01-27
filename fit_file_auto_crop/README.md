FIT file auto cropper
=====================

Vapourware tools to explore and munge .fit.gz files from a Strava activities export.

Dependencies
------------

This is vapourware and mostly undocumented/unsupported, but you need Python, uv, and optionally direnv.

Functionality:
--------------

`find_suspicious_activities.py`

Iterate .fit.gz files exported from Strava, and identify those with suspiciously fast segments. Writes out the suspicious activities to a CSV

It uses https://github.com/polyvertex/fitdecode to decode Python files, which is a more performant fork of https://github.com/dtcooper/python-fitparse. The code in this repo also makes some effort to not do anything too slow, but if you want to analyze thousands of files then it's still going to take a long time. There are open source libraries out there in C, Rust and Java.

`crop_activities.py`

Reads a CSV of activities identified as suspicious. Opens each .fit.gz in turn, and tries to find a record which comes back to within 10 metres of the start point. It then writes out a cropped version of the file, ending at this point.

`wiggles_finder.py`

Uses polars to munge the data based on changes in direction and speed, then writes out a JSON file for use with `wiggles_viewer.html`

`wiggles_viewer.html`

For viewing the wiggles on OpenStreetMap. Requires a local directory named wiggles_json with the JSON files, which is ignored by git (you can also add a symlink to smewhere else). First start a server with:

`python -m http.server 8000`

to avoid CORS issues when fetching JSON files. Then load a file for viewing in the browser address bar like this:

http://0.0.0.0:8000/wiggles_viewer.html?file=wiggles_5817061951.json


Perhaps one day this project will be extended to auto-cropping based on patterns in the wiggles, probably not though