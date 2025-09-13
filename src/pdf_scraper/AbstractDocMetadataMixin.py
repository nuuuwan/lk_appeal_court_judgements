import inspect
import os
import pathlib
from dataclasses import asdict
from functools import cache, cached_property

from utils import JSONFile, Log

log = Log("AbstractDocMetadataMixin")


class AbstractDocMetadataMixin:
    @cached_property
    def dir_doc(self) -> str:
        return os.path.join(
            self.get_dir_docs_root(), self.decade, self.year, self.doc_id
        )

    @cached_property
    def json_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.json")

    def write(self):
        if os.path.exists(self.json_path):
            return
        os.makedirs(self.dir_doc, exist_ok=True)
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
    @cache
    def list_all(cls):
        doc_list = [
            cls.from_file(json_path) for json_path in cls.get_all_json_paths()
        ]
        doc_list.sort(key=lambda doc: (doc.doc_id), reverse=True)
        return doc_list

    @classmethod
    @cache
    def year_to_month_to_doc_list(
        cls,
    ) -> dict[str, dict[str, list]]:
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
