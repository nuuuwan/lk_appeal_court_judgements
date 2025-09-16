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
    def get_doc_class_label(cls):
        return "appeals"

    @classmethod
    def doc_class_pretty_label(cls) -> str:
        return "⚖️ Judgements of the Court of Appeal of 🇱🇰 Sri Lanka"

    @classmethod
    def get_remote_data_url_base(cls) -> str:
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
                self.get_remote_data_url_base(),
                self.__class__.get_dir_docs_for_cls_relative(),
                self.dir_doc_relative_to_class,
            ]
        )

    @classmethod
    def gen_docs(cls) -> Generator["AppealsDoc", None, None]:
        for data_page in AppealsHomePage().gen_data_pages():
            for d in data_page.gen_dicts():
                yield cls(**d)
