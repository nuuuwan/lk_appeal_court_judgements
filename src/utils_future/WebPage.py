from functools import cached_property

import requests
from bs4 import BeautifulSoup


class WebPage:
    TIMEOUT = 120

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"🌐 {self.url}"

    @cached_property
    def html(self):
        response = requests.get(self.url, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.text

    @cached_property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")
