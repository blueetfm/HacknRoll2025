import json

import scrapy
from typing import Any, Dict, Iterable
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from scrapy import Field, Item

USER_AGENT = "Python/3. Scrapy/2.11"


class MysteryPictureAPIItem(Item):
    api_response = Field()


class MysteryPictureSpider(scrapy.Spider):
    name = "mystery-picture-spider"
    custom_settings = {"KAFKA_TOPIC": KAFKA_TOPIC_MYSTERY_PICTURE}
    batch_size = 50

    def start_requests(self) -> Iterable[Request]:
        yield Request(
            url="http://localhost:9999/rows/0",
            headers={"User-Agent": USER_AGENT},
            meta={"page": 0}  # pass an initial page number of 1 in the metadata
        )


    def parse(self, response: Response, **kwargs: Any) -> Any:
        # send raw HTML from the page to the Kafka
        yield MysteryPictureAPIItem(api_response=str(response.text))

        # Derive the next page from the request's metadata
        next_page = int(response.meta["page"]) + 1
        if next_page < 500:
            # if (what looks like) the link to the webpage is in the response HTML, we're not on the last page,
            # so yield another Request to scrape the next page
            yield Request(
                url=f"http://localhost:9999/rows/{next_page}",
                headers={"User-Agent": USER_AGENT},
                meta={"page": next_page}
            )