from functools import cached_property

import requests
from bs4 import BeautifulSoup
from utils import Log

log = Log("WebPage")


class WebPage:
    TIMEOUT = 120

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"🌐 {self.url}"

    @cached_property
    def html(self):
        log.debug(f"[{self}] Openning...")
        response = requests.get(self.url, timeout=self.TIMEOUT)
        response.raise_for_status()
        content = response.text
        n_content = len(content)
        log.debug(f"[{self}] Opened. {n_content:,}B")
        return content

    @cached_property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")
