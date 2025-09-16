from itertools import chain
from typing import Generator

from utils import Log

from appeals.pages.AppealsDataPage import AppealsDataPage
from appeals.pages.AppealsHomePageNewMixin import AppealsHomePageNewMixin
from appeals.pages.AppealsHomePageOldMixin import AppealsHomePageOldMixin
from utils_future import WWW

log = Log("AppealsHomePage")


class AppealsHomePage(WWW, AppealsHomePageNewMixin, AppealsHomePageOldMixin):
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

    def gen_data_pages(self) -> Generator[AppealsDataPage, None, None]:
        if self.soup is None:
            return
        yield from chain(
            self.__gen_data_pages_new__(), self.__gen_data_pages_old__()
        )
