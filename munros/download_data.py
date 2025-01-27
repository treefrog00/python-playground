from bs4 import BeautifulSoup
import httpx
import os
from urllib.parse import urljoin
import pathlib
from pathlib import Path
import asyncio
import sys

sem = asyncio.Semaphore(4)

# Base URL for relative links
base_url = "https://www.stevenfallon.co.uk"

base_data_folder = Path(os.getenv("SCRAPED_DATA_FOLDER"))

async def async_fetch(client, download_dir, link):
    full_url = urljoin(base_url, link)
    filename = os.path.join(download_dir, link)

    if Path(filename).exists():
        return
    print(full_url)
    async with sem:
        response = await client.get(full_url)
        response.raise_for_status()
    with open(filename, 'w') as f:
        f.write(response.text)
    print(f"Successfully downloaded to: {filename}")

async def download_links(links, download_dir):
    os.makedirs(download_dir, exist_ok=True)

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[async_fetch(client, download_dir, link) for link in links])


def munros_part_one():
    download_dir = base_data_folder / "downloaded_munros"

    with open(base_data_folder / "Munros listed by name _ Steven Fallon.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    hindents = soup.find_all('div', class_='hindent')

    all_links = []
    for hindent_div in hindents:
        links = hindent_div.find_all('a')
        for link in links:
            relative_url = link.get('href')
            print(relative_url)
            text = link.text.strip()
            all_links.append(relative_url)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_links(all_links, download_dir))


def munros_part_two():
    route_download_dir = base_data_folder / "downloaded_munros_routes"

    # note there are two copies of each link in the route summary table
    route_links = set()

    for f in pathlib.Path("downloaded_munros").iterdir():
        with open(f) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        # sometimes there are multiple route summary tables stacked together
        summary_tables = soup.find_all('table', class_='routesummarytable')

        if summary_tables:
            for summary in summary_tables:
                page_links = [link.get("href") for link in summary.find_all("a")]
                route_links.update(page_links)
        else:
            print(f"no route summary for {f}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_links(route_links, route_download_dir))

def corbetts_part_one():
    download_dir = base_data_folder / "downloaded_corbetts"

    with open(base_data_folder / "Corbetts listed by name alphabetically _ Steven Fallon.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    hindents = soup.find_all('div', class_='hindent')

    all_links = []
    for hindent_div in hindents:
        links = hindent_div.find_all('a')
        for link in links:
            relative_url = link.get('href')
            print(relative_url)
            text = link.text.strip()
            # fix typo in url
            if relative_url == "sgurr-dhomhnuill.html":
                relative_url = "sgurr-dhomhuill.html"
            all_links.append(relative_url)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_links(all_links, download_dir))


def corbetts_part_two():
    route_download_dir = base_data_folder / "downloaded_corbetts_routes"

    # note there are two copies of each link in the route summary table
    route_links = set()

    for f in pathlib.Path("downloaded_munros").iterdir():
        with open(f) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        # sometimes there are multiple route summary tables stacked together
        summary_tables = soup.find_all('table', class_='routesummarytable')

        if summary_tables:
            for summary in summary_tables:
                page_links = [link.get("href") for link in summary.find_all("a")]
                route_links.update(page_links)
        else:
            print(f"no route summary for {f}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_links(route_links, route_download_dir))

if __name__ == "__main__":
    help_msg = "Usage: python download_data.py --munros-part-one|--munros-part-two|...or corbetts"
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)

    if sys.argv[1] == "--munros-part-one":
        munros_part_one()
    elif sys.argv[1] == "--munros-part-two":
        munros_part_two()
    elif sys.argv[1] == "--corbetts-part-one":
        corbetts_part_one()
    elif sys.argv[1] == "--corbetts-part-two":
        corbetts_part_two()
    else:
        print(help_msg)
        sys.exit(1)

