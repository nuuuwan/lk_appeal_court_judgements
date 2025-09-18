from dataclasses import dataclass
from typing import Generator

from appeals.pages import AppealsHomePage
from scraper import AbstractPDFDoc


@dataclass
class AppealsDoc(AbstractPDFDoc):
    parties: str
    judgement_by: str
    keywords: str
    legistation: str

    @classmethod
    def gen_docs(cls) -> Generator["AppealsDoc", None, None]:
        for data_page in AppealsHomePage().gen_data_pages():
            for d in data_page.gen_dicts():
                yield cls(**d)
