from typing import Generator

from appeals.AppealsDoc import AppealsDoc
from pdf_scraper import AbstractDataPage


class AppealsDataPage(AbstractDataPage):

    @staticmethod
    def __parse_tr__(tr) -> AppealsDoc:
        tds = tr.find_all("td")

        num = tds[1].get_text().strip()

        date_str = tds[0].get_text().strip()
        assert len(date_str) == 10

        url_pdf = tds[6].find("a")["href"]
        assert url_pdf.endswith(".pdf")

        parties = tds[2].get_text().strip()
        judgement_by = tds[3].get_text().strip()
        keywords = tds[4].get_text().strip()
        legistation = tds[5].get_text().strip()

        return AppealsDoc(
            # from AbstractDoc
            num=num,
            date_str=date_str,
            description="",
            url_pdf=url_pdf,
            # specific
            parties=parties,
            judgement_by=judgement_by,
            keywords=keywords,
            legistation=legistation,
        )

    def gen_docs(self) -> Generator[AppealsDoc]:
        tbody = self.soup.find("table").find("tbody")
        for tr in tbody.find_all("tr"):
            doc = self.__parse_tr__(tr)
            yield doc
