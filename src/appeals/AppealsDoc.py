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
                "An appeals court judgment (also called an appellate court judgment) is a ruling delivered by a higher court that reviews decisions made by lower courts. It ensures that justice is applied consistently, correcting legal or procedural errors that may have occurred at trial.",  # noqa: E501
                "In Sri Lanka, the Court of Appeal plays this role, shaping how laws are interpreted and setting important legal precedents that influence future cases. These judgments are central to upholding fairness, protecting rights, and strengthening the rule of law.",  # noqa: E501
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
