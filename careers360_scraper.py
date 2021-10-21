import csv
import sys

import requests
from scrapy.http import HtmlResponse
from scrapy.selector import Selector


def get_details_from_response(response):
    div_class = "cardBlk"
    xpath = f"//div[contains(@class, '{div_class}')]/div[@class='cardContent']/div[@class='content']"
    xpath_college_name = "h2[@class='blockHeading']/a/text()"
    xpath_college_city = "ul[@class='rank'][1]/li[1]/a[1]/text()"
    xpath_college_state = "ul[@class='rank'][1]/li[1]/a[2]/text()"

    selector = Selector(response=response)

    cards = selector.xpath(xpath)

    count = 0

    for card in cards:
        name = card.xpath(xpath_college_name).get()
        city = card.xpath(xpath_college_city).get()
        state = card.xpath(xpath_college_state).get()

        details = {
            "Name": str(name),
            "City": str(city),
            "State": str(state),
        }

        yield details
        count += 1

    return count


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 careers360_scraper.py PAGES OUTPUT_FILE")
        sys.exit(1)

    pages = int(sys.argv[1])
    output_file = sys.argv[2]

    base_url = "https://engineering.careers360.com/colleges/list-of-engineering-colleges-in-india"

    with open(output_file, "w") as csv_file:
        dw = csv.DictWriter(csv_file, ["Name", "City", "State"])
        dw.writeheader()

        for page in range(1, pages+1):
            url = f"{base_url}?page={page}"

            r = requests.get(url)
            response = HtmlResponse(url=url, body=r.content)

            for college_details in get_details_from_response(response):
                dw.writerow(college_details)

            print(f"Page {page} done")
