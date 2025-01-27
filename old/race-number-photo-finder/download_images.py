import argparse
import requests
from bs4 import BeautifulSoup


class WebPages:
    ironwood_2018 = "http://www.nailsearunningclub.org.uk/ironwood-challenge-2018/"


def download_images_for_page(page):
    images = page.find_all('img[')

def main():
    parser = argparse.ArgumentParser(description="Download race pictures.")
    parser.add_argument("dest", help="dest dir")

    args = parser.parse_args()

    root_page = WebPages.ironwood_2018

    page = requests.get(root_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    download_images_for_page(soup)

    for link in soup.select(".ngg-navigation a.page-numbers"):
        page_data = requests.get(link["href"])
        download_images_for_page(page_data)


if __name__ == "__main__":
    main()
