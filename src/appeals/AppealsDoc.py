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
    def get_doc_class_description(cls) -> str:
        return "\n\n".join(
            [
                "A Court of Appeal judgment is a higher court ruling that reviews decisions of lower courts, shaping legal precedent and protecting citizens’ rights.",  # noqa: E501
            ]
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "⚖️"

    @classmethod
    def gen_docs(cls) -> Generator["AppealsDoc", None, None]:
        for data_page in AppealsHomePage().gen_data_pages():
            for d in data_page.gen_dicts():
                yield cls(**d)
