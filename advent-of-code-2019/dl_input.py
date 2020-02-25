import requests
import argparse
from os.path import expanduser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('day')
    parser.add_argument('session')
    return parser.parse_args()


args = parse_args()

url = 'https://adventofcode.com/2019/day/{}/input'.format(args.day)
cookies = {
    "session": args.session
}

r = requests.get(url, allow_redirects=True, cookies=cookies)

open(expanduser('~/tmp/2019/day{}.txt'.format(args.day)), 'wb').write(r.content)