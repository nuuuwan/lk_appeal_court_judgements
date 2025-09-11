from itertools import chain
from typing import Generator
from urllib.parse import quote

from utils import Log

from appeals.AppealsDataPage import AppealsDataPage
from appeals.AppealsOldDataPage import AppealsOldDataPage
from pdf_scraper import AbstractHomePage

log = Log("AppealsHomePage")


class AppealsHomePage(AbstractHomePage):
    def __init__(self):
        super().__init__("https://courtofappeal.lk")

    def get_judgements_menu_item(self):
        menu_items = self.soup.find_all(
            "li",
            class_="menu-item",
        )
        for menu_item in menu_items:
            for a in menu_item.find_all("a", recursive=False):
                if "Judgments" in a.text:
                    log.debug("✅ Found Judgements menu item.")
                    return menu_item

        raise ValueError("Could not find Judgements menu item")

    def gen_data_pages_new(self) -> Generator[AppealsDataPage, None, None]:
        judgements_menu_item = self.get_judgements_menu_item()
        ul = judgements_menu_item.find(
            "ul", class_="sub-menu", recursive=False
        )
        for li_year in ul.find_all("li", recursive=False):
            year = li_year.find("a").text.strip()
            log.debug(f"{year=}")
            ul_year = li_year.find("ul", class_="sub-menu", recursive=False)
            if not ul_year:
                continue
            for li_month in ul_year.find_all("li", recursive=False):
                a_month = li_month.find("a")
                month_str = a_month.text.strip()
                log.debug(f"{year=}, {month_str=}")
                url = a_month["href"]
                if url == "#":
                    continue
                if not url.startswith("http"):
                    url = self.url + quote(url)
                url = quote(url, safe=":/?&=%")
                yield AppealsDataPage(url, year, month_str)

    def gen_data_pages_old(self) -> Generator[AppealsDataPage, None, None]:
        judgements_menu_item = self.get_judgements_menu_item()
        ul = judgements_menu_item.find(
            "ul", class_="sub-menu", recursive=False
        )

        for li_year_or_older_judgements in ul.find_all("li", recursive=False):
            text = li_year_or_older_judgements.find("a").text.strip()
            if text != "Older Judgments":
                continue
            ul_older_judgements = li_year_or_older_judgements.find(
                "ul", class_="sub-menu", recursive=False
            )
            for li_year in ul_older_judgements.find_all("li", recursive=False):
                year = li_year.find("a").text.strip()
                log.debug(f"{year=}")
                ul_year = li_year.find(
                    "ul", class_="sub-menu", recursive=False
                )
                if not ul_year:
                    continue
                for li_month in ul_year.find_all("li", recursive=False):
                    a_month = li_month.find("a")
                    month_str = a_month.text.strip()
                    log.debug(f"{year=}, {month_str=}")
                    url = a_month["href"]
                    if url == "#":
                        continue
                    if not url.startswith("http"):
                        url = self.url + quote(url)
                    url = quote(url, safe=":/?&=%")
                    yield AppealsOldDataPage(url, year, month_str)

    def gen_data_pages(self) -> Generator[AppealsDataPage, None, None]:
        # HACK Temp Disable New
        # yield from chain(self.gen_data_pages_new(), self.gen_data_pages_old())
        yield from chain(self.gen_data_pages_old())
