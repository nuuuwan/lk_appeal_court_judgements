import inspect
import os
import pathlib
import re
from abc import ABC
from dataclasses import asdict, dataclass
from functools import cache, cached_property

from utils import Hash, JSONFile, Log

log = Log("AbstractDoc")


@dataclass
class AbstractDoc(ABC):
    num: str
    date_str: str
    description: str
    url_pdf: str

    @classmethod
    @cache
    def doc_class_label(cls) -> str:
        class_name = cls.__name__
        assert class_name.endswith("Doc")
        return class_name[:-3].lower()

    @classmethod
    @cache
    def get_dir_docs_root(cls) -> str:
        return os.path.join(
            "data",
            cls.doc_class_label(),
        )

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
    def year_and_month(self) -> str:
        assert len(self.date_str) == 10
        return self.date_str[:7]

    @cached_property
    def dir_doc(self) -> str:
        return os.path.join(
            self.get_dir_docs_root(), self.decade, self.year, self.doc_id
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

    @classmethod
    def get_all_json_paths(cls) -> list[str]:
        return [
            str(json_path)
            for json_path in pathlib.Path(cls.get_dir_docs_root()).rglob(
                "doc.json"
            )
        ]

    @classmethod
    def from_file(cls, json_path: str):
        data = JSONFile(json_path).read()
        sig = inspect.signature(cls.__init__)
        valid_keys = set(sig.parameters) - {"self"}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    @classmethod
    def list_all(cls):
        doc_list = [
            cls.from_file(json_path) for json_path in cls.get_all_json_paths()
        ]
        doc_list.sort(key=lambda doc: (doc.doc_id), reverse=True)
        return doc_list

    @classmethod
    def year_to_month_to_doc_list(
        cls,
    ) -> dict[str, dict[str, list["AbstractDoc"]]]:
        idx = {}
        for doc in cls.list_all():
            year = doc.year
            year_and_month = doc.year_and_month

            if year not in idx:
                idx[year] = {}
            if year_and_month not in idx[year]:
                idx[year][year_and_month] = []

            idx[year][year_and_month].append(doc)
        return idx
