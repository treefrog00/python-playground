from itertools import chain
from bs4 import BeautifulSoup
import pathlib
from pathlib import Path
import re
from pyproj import Transformer
from bng import to_osgb36
import json
from pathlib import Path
import os

crs_british = 'EPSG:27700'
crs_wgs84 = 'EPSG:4326'

transformer = Transformer.from_crs(crs_british, crs_wgs84)

base_data_folder = Path(os.getenv("SCRAPED_DATA_FOLDER"))

def fix_grid_ref_typos(val):
    # some of the grid refs have typos
    # using the links to google maps:
    # NG97757 (eighe) should be 57.5648501,-5.3833154
    # that converts to NG977577
    # N0310852 should be 56.9527229,-3.1356062
    # that converts to NO310851
    # N0156881 I'm just assuming the 0 should be a O

    return (val
    .replace("NG97757", "NG977577")
    .replace("N0310852", "NO310851")
    .replace("N0156881", "NO156881")
    )

name_translate_table = {
    "Ben Alder": "Aonach Beag (Ben Alder)",
}

def translate_munro_name(name, fname):
    if name == "A' Chailleach":
        if fname.startswith("fann"):
            return "A' Chailleach (Fannaichs)"
        elif fname.startswith("monad"):
            return "A' Chailleach (Monadh Liath)"
        raise Exception()
    if name in ("Geal Charn", "Geal-charn"):
        if fname.startswith("drumochter"):
            return "Gael-Charn (Drumochter)"
        elif fname.startswith("monad"):
            return "Geal-Chàrn (Monadhliath)"
        return "Geal-Charn (one or the other)"
    if name in name_translate_table:
        return name_translate_table[name]
    return name

def parse_summits(summits, fname):
    summits = re.sub("\([^)]+\)", "", summits)
    summits = re.split("\n\s+|,| \n", summits)
    summits = [m.strip() for m in summits]
    summits = [m for m in summits if m]
    summits = [translate_munro_name(m, fname) for m in summits]

    return summits

def extract_table(table, f):
    results = {
        "file": f.name,
    }

    key_replace = {
        "Nav": "Navigation",
    }

    for row in table.find_all('tr', recursive=False):
        aux = row.find_all('td')
        if len(aux) < 2:
            continue
        key = aux[0].text.strip()

        for key_to_change, replacement in key_replace.items():
            if key == key_to_change:
                key = replacement

        # hackily parse results with sub tables for walk/bike
        if key in ("distance", "time"):
            if f"Walk {key}" in results:
                key = f"Bike {key}"
            else:
                key = f"Walk {key}"

        if key in ["Terrain", "Navigation", "Effort", "Scenery"]:
            img_src = aux[1].find("img").get("src")
            val = int(re.search("\d+", img_src).group(0))
        elif key == "Distance":
            val = aux[1].text.strip()
            match = re.search("([\d.]+)km", val)
            if not match:
                print(val)
            val = float(match.group(1))
        elif key in ("Ascent", "Walk ascent", "Bike ascent"):
            val = aux[1].text.strip()
            match = re.search("(\d+)m", val)
            if not match:
                print(val)
            val = int(match.group(1))
        elif key in ("Munros", "Corbetts", "Grahams"):
            val = parse_summits(aux[1].text.strip(), f.name)
        else:
            replace_chars = ["\xa0", "\t", "\n"]
            val = aux[1].text.strip()
            for char in replace_chars:
                val = val.replace(char, " ")
                val = re.sub("\s+", " ", val)

        if key == "Start" or key == "Start/finish":
            val = fix_grid_ref_typos(val)
            os_match = re.search(": ([A-Z]{2}\d{3}\d{3})", val)
            if not(os_match):
                print(f.name)
                return results
            os_numeric = to_osgb36(os_match.group(1))
            lat_lon = transformer.transform(*os_numeric)
            results["lat_lon"] = lat_lon

        results[key] = val

    if "Profile" in results:
        del results["Profile"]

    return results

def run(mountain_type, mountains_folder, routes_folder):
    datas = []

    for f in sorted((base_data_folder / mountains_folder).iterdir()):
        with open(f) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        route_summary = soup.find('table', class_='routesummarytable')

        if not route_summary:
            tables = soup.find_all("table")
            print(f)
            route = extract_table(tables[0], f)
            if "Terrain" not in route:
                extra_data = extract_table(tables[1], f)
                route.update(extra_data)

            datas.append(route)

    for f in sorted((base_data_folder / routes_folder).iterdir()):
        with open(f) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        table = soup.find('table')
        route = extract_table(table, f)

        datas.append(route)

    return datas

if __name__ == "__main__":
    munro_data = run("munro", "downloaded_munros", "downloaded_munros_routes")

    corbett_data = run("corbett", "downloaded_corbetts", "downloaded_corbetts_routes")

    # put in dict by file to eliminate duplicates across munros/corbetts data
    data = {
        m["file"]: m for m in chain(munro_data, corbett_data)
    }

    for i, d in enumerate(data.values()):
        d["id"] = i

    with open("fallon_data.json", 'w') as f:
        f.write(json.dumps(list(data.values()), indent=2))
