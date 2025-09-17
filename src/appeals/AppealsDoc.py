from dataclasses import dataclass
from functools import cache, cached_property
from typing import Generator

from appeals.pages import AppealsHomePage
from pdf_scraper import AbstractDoc


@dataclass
class AppealsDoc(AbstractDoc):
    parties: str
    judgement_by: str
    keywords: str
    legistation: str

    @classmethod
    def gen_docs(cls) -> Generator["AppealsDoc", None, None]:
        for data_page in AppealsHomePage().gen_data_pages():
            for d in data_page.gen_dicts():
                yield cls(**d)
