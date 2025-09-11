from typing import Generator

from appeals.AppealsDoc import AppealsDoc
from pdf_scraper import AbstractDataPage


class AppealsDataPage(AbstractDataPage):

    def gen_docs(self) -> Generator[AppealsDoc]:
        return []
