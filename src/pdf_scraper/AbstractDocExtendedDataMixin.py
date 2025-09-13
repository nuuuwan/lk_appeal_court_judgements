import os
import shutil
from functools import cached_property

import requests
from utils import Log

log = Log("AbstractDocExtendedDataMixin")


class AbstractDocExtendedDataMixin:
    T_TIMEOUT_PDF_DOWNLOAD = 120

    @cached_property
    def dir_doc_extended(self) -> str:
        dir_metadata = os.path.basename(os.getcwd())
        return os.path.join(
            "..",
            f"{dir_metadata}_data",
            self.get_dir_docs_root(),
            self.decade,
            self.year,
            self.doc_id,
        )

    def __copy_metadata__(self):
        shutil.copytree(
            self.dir_doc, self.dir_doc_extended, dirs_exist_ok=True
        )

    @cached_property
    def pdf_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "en.pdf")

    def __download_pdf__(self):
        url = self.url_pdf
        log.debug(f"Downloading {url} -> {self.pdf_path}")
        response = requests.get(url, timeout=self.T_TIMEOUT_PDF_DOWNLOAD)
        response.raise_for_status()
        with open(self.pdf_path, "wb") as f:
            f.write(response.content)
        log.info(f"Wrote {self.pdf_path}")

    def scrape_extended_data(self):
        if not os.path.exists(self.dir_doc):
            os.makedirs(self.dir_doc_extended)
            self.__copy_metadata__()
        if not os.path.exists(self.pdf_path):
            self.__download_pdf__()
