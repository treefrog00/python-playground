Munro + Corbett walks
=====================

This project consists of

a) some Python scripts to scrape and munge data all the suggested Munro walks by Steven Fallon.

It extracts distances/ascent metres/timings, converts OS grid references to lat/lon coords, and converts the images used by Steven Fallon to represent varying difficulty of terrain/navigation/etc to numerical values.

This data is then munged and combined into a JSON file.

b) a web frontend using Leaflet.js, that loads the JSON and displays pins on OpenStreetMap. Walks are color-coded with pins according to how difficult there are in terms of terrain + effort, and walks where the itinerary includes cycling are given a cycle icon on the map. On clicking a pin you are provided with a link to Steven's website.

To run the web server using the included data:

(there is no backend, this is just to avoid CORS issues with loading JSON from a file):

```
python3 -m http.server
```

Then open:

http://localhost:8000/munros.html

If you wish to modify the underlying data, the data transformation backend consists of a series of Python scripts.

Prequisites for data scraping + transformation:
* Python
* install uv
* create a data folder and create a .env file based on .env.template that points to it
* manually download "Corbetts listed by name alphabetically _ Steven Fallon.html" and "Munros listed by name _ Steven Fallon.html" to your data folder

* either install direnv, or otherwise manually load the env with:

```
source .venv/bin/activate
set -a
source .env
set +a
```

Then:
```
uv sync
create .env based on .env.template

python download_data.py --munros-part-one
python download_data.py --munros-part-two
python download_data.py --corbetts-part-one
python download_data.py --corbetts-part-two
python extract_data.py
python create_icons.py
```

To run web server

Attribution:
- the scraped data is copyright Steve Fallon
- the bike icon is Creative Commons non-commercial use, Laura Lin, from Noun project