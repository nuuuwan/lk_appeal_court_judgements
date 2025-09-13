from typing import Generator
from urllib.parse import quote

from utils import Log

from appeals.AppealsDataPage import AppealsDataPage

log = Log("AppealsHomePageNewMixin")


class AppealsHomePageNewMixin:
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
