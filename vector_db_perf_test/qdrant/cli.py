from shared.profile_ingestion import time_ingest_many
from hello import QdrantDb
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=Path)
parser.add_argument('--ext')
parser.add_argument('--one-giant-doc', default=False, action='store_true')
parser.add_argument('--exclude', nargs='+', default=[])
args = parser.parse_args()
dir = args.dir

exclude = set(args.exclude)

time_ingest_many(dir.glob(f"**/*.{args.ext}"), QdrantDb(dir.stem), args.one_giant_doc, exclude)