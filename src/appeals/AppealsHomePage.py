from typing import Generator

from utils import Log

from appeals.AppealsDataPage import AppealsDataPage
from pdf_scraper import AbstractHomePage

log = Log("AppealsHomePage")


class AppealsHomePage(AbstractHomePage):
    def __init__(self):
        super().__init__("https://courtofappeal.lk/")

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

    def gen_data_pages(self) -> Generator[AppealsDataPage]:
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
                month = a_month.text.strip()
                log.debug(f"{month=}")
                url = a_month["href"]
                if url == "#":
                    continue
                yield AppealsDataPage(url)
