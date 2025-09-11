import os
import re
from abc import ABC
from dataclasses import asdict, dataclass
from functools import cached_property

from utils import Hash, JSONFile, Log

log = Log("AbstractDoc")


@dataclass
class AbstractDoc(ABC):
    num: str
    date_str: str
    description: str
    url_pdf: str

    @cached_property
    def num_short(self):
        if len(self.num) < 32:
            return self.num
        h = Hash.md5(self.num)
        return f"{self.num[:23]}-{h}[:8]"

    @cached_property
    def doc_id(self):
        doc_id = f"{self.date_str}-{self.num_short}"
        doc_id = re.sub(r"[^a-zA-Z0-9\-]", "-", doc_id)
        return doc_id

    @cached_property
    def decade(self) -> str:
        assert len(self.date_str) == 10
        return self.date_str[:3] + "0s"

    @cached_property
    def year(self) -> str:
        assert len(self.date_str) == 10
        return self.date_str[:4]

    @cached_property
    def dir_doc(self) -> str:
        return os.path.join(
            "data", "docs", self.decade, self.year, self.doc_id
        )

    @cached_property
    def json_path(self) -> str:
        os.makedirs(self.dir_doc, exist_ok=True)
        return os.path.join(self.dir_doc, "doc.json")

    def write(self):
        JSONFile(self.json_path).write(
            dict(doc_id=self.doc_id) | asdict(self)
        )
        log.info(f"Wrote {self.json_path}")
