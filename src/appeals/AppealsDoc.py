from dataclasses import dataclass
from functools import cache, cached_property

from pdf_scraper import AbstractDoc


@dataclass
class AppealsDoc(AbstractDoc):
    parties: str
    judgement_by: str
    keywords: str
    legistation: str

    @classmethod
    @cache
    def doc_class_pretty_label(cls) -> str:
        return "⚖️ Judgements of the Court of Appeal of 🇱🇰 Sri Lanka"

    @classmethod
    @cache
    def remote_data_url_base(cls) -> str:
        return "/".join(
            [
                "https://github.com",
                "nuuuwan",
                "lk_judiciary_appeals_court",
                "tree",
                "data",  # branch-name
            ]
        )

    @cached_property
    def remote_data_url(self) -> str:
        return "/".join(
            [
                self.remote_data_url_base(),
                self.dir_doc_extended_without_base,
            ]
        )
