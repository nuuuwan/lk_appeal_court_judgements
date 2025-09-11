import re
from functools import cached_property
from typing import Generator
from urllib.parse import quote

from utils import Log

from appeals.AppealsDoc import AppealsDoc
from pdf_scraper import AbstractDataPage

log = Log("AppealsDataPage")


class AppealsDataPage(AbstractDataPage):

    def __init__(self, url: str, year: str, month_str: str):
        super().__init__(url)
        self.year = year
        self.month_str = month_str

    @staticmethod
    def clean_text(x):
        x = re.sub(r"\s+", " ", x)
        x = x.strip()
        return x

    @cached_property
    def month(self):
        return {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12",
        }[self.month_str]

    def __parse_tr__(self, tr) -> AppealsDoc:
        tds = tr.find_all("td")
        text_list = [self.clean_text(td.get_text()) for td in tds]

        num = text_list[1]
        if not num:
            log.warning(f"Skipping row with empty num: {tr}")
            return None

        date_str = text_list[0]
        assert len(date_str) == 10 or date_str == "N/A"

        if date_str == "N/A":
            date_str = f"{self.year}-{self.month}-NA"

        url_pdf = tds[6].find("a")["href"]
        assert url_pdf.endswith(".pdf")
        if not url_pdf.startswith("http"):
            url_pdf = "https://courtofappeal.lk" + url_pdf
        url_pdf = quote(url_pdf, safe=":/?&=%")

        parties = text_list[2]
        judgement_by = text_list[3]
        keywords = text_list[4]
        legistation = text_list[5]

        description = f"{parties} before {judgement_by}"

        return AppealsDoc(
            # from AbstractDoc
            num=num,
            date_str=date_str,
            description=description,
            url_pdf=url_pdf,
            # specific
            parties=parties,
            judgement_by=judgement_by,
            keywords=keywords,
            legistation=legistation,
        )

    def gen_docs(self) -> Generator[AppealsDoc, None, None]:
        table = self.soup.find("table")
        if not table:
            return
        tbody = table.find("tbody")
        for tr in tbody.find_all("tr"):
            doc = self.__parse_tr__(tr)
            if doc:
                yield doc
