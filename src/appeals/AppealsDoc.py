from dataclasses import dataclass
from functools import cache

from pdf_scraper import AbstractDoc


@dataclass
class AppealsDoc(AbstractDoc):
    parties: str
    judgement_by: str
    keywords: str
    legistation: str

    @classmethod
    @cache
    def doc_class_description(cls) -> str:
        return (
            "Judgements of the Court of Appeal of Sri Lanka,"
            + " downloaded from"
            + " [https://courtofappeal.lk](https://courtofappeal.lk)."
        )
