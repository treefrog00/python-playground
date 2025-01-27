from pathlib import Path
import json
from itertools import chain
import re

mapping = {
}

with Path('fallon_data.json').open() as f:
    fdata = json.load(f)

with Path('wiki_data.json').open() as f:
    wdata = json.load(f)

trans = str.maketrans("àìùò","aiuo")

def normalize(name):
    return name.translate(trans)

wn = set(normalize(w["Name"]) for w in wdata)
fn = set(chain.from_iterable(x["Munros"] for x in fdata if "Munros" in x))

needs_custom_match = wn - fn

all_ids = {v["id"] for v in fdata}

easy = set(v["id"] for v in fdata if v["Effort"] < 5 and v["Terrain"] < 5)
hard_effort_and_terrain = set(v["id"] for v in fdata if v["Effort"] > 5 and v["Terrain"] > 5)
hard_effort_only = set(v["id"] for v in fdata if v["Effort"] > 5) - hard_effort_and_terrain
hard_terrain_only = set(v["id"] for v in fdata if v["Terrain"] > 5) - hard_effort_and_terrain
medium = all_ids - easy - hard_effort_and_terrain - hard_effort_only - hard_terrain_only

print("counts")
counts = {
    'easy': len(easy),
    'hard_effort_and_terrain': len(hard_effort_and_terrain),
    'hard_effort_only': len(hard_effort_only),
    'hard_terrain_only': len(hard_terrain_only),
    'medium': len(medium)
}

for category, count in counts.items():
    print(f"{category}: {count}")

