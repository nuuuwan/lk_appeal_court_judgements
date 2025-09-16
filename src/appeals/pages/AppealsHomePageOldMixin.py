from typing import Generator
from urllib.parse import quote

from utils import Log

from appeals.pages.AppealsOldDataPage import AppealsOldDataPage

log = Log("AppealsHomePageOldMixin")


class AppealsHomePageOldMixin:
    def __parse_old_li_month__(
        self, li_month, year
    ) -> Generator[AppealsOldDataPage, None, None]:
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
    ) -> Generator[AppealsOldDataPage, None, None]:
        year = li_year.find("a").text.strip()
        log.debug(f"{year=}")
        ul_year = li_year.find("ul", class_="sub-menu", recursive=False)
        if not ul_year:
            return
        for li_month in ul_year.find_all("li", recursive=False):
            yield from self.__parse_old_li_month__(li_month, year)

    def __gen_data_pages_old__(
        self,
    ) -> Generator[AppealsOldDataPage, None, None]:
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
            for li_year in ul_older_judgements.find_all("li", recursive=False):
                yield from self.__parse_old_li_year__(li_year)
