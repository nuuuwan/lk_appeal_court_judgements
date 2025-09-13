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

    def __get_judgements_menu_item__(self):
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

    def __parse_new_li_month__(
        self, li_month, year
    ) -> Generator[AppealsDataPage, None, None]:
        a_month = li_month.find("a")
        month_str = a_month.text.strip()
        log.debug(f"{year=}, {month_str=}")
        url = a_month["href"]
        if url == "#":
            return
        if not url.startswith("http"):
            url = self.url + quote(url)
        url = quote(url, safe=":/?&=%")
        yield AppealsDataPage(url, year, month_str)

    def __gen_data_pages_new__(
        self,
    ) -> Generator[AppealsDataPage, None, None]:
        judgements_menu_item = self.__get_judgements_menu_item__()
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
                yield from self.__parse_new_li_month__(li_month, year)

    def __parse_old_li_month__(
        self, li_month, year
    ) -> Generator[AppealsDataPage, None, None]:
        a_month = li_month.find("a")
        month_str = a_month.text.strip()
        log.debug(f"{year=}, {month_str=}")
        url = a_month["href"]
        if url == "#":
            return
        if not url.startswith("http"):
            url = self.url + quote(url)
        url = quote(url, safe=":/?&=%")
        yield AppealsOldDataPage(url, year, month_str)

    def __parse_old_li_year__(
        self, li_year
    ) -> Generator[AppealsDataPage, None, None]:
        year = li_year.find("a").text.strip()
        log.debug(f"{year=}")
        ul_year = li_year.find("ul", class_="sub-menu", recursive=False)
        if not ul_year:
            return
        for li_month in ul_year.find_all("li", recursive=False):
            yield from self.__parse_old_li_month__(li_month, year)

    def __gen_data_pages_old__(
        self,
    ) -> Generator[AppealsDataPage, None, None]:
        judgements_menu_item = self.__get_judgements_menu_item__()
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
            for li_year in ul_older_judgements.find_all(
                "li", recursive=False
            ):
                yield from self.__parse_old_li_year__(li_year)

    def gen_data_pages(self) -> Generator[AppealsDataPage, None, None]:
        if self.soup is None:
            return
        yield from chain(
            self.__gen_data_pages_new__(), self.__gen_data_pages_old__()
        )
