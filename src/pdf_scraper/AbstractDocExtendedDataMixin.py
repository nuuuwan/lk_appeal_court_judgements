import os
import shutil
from functools import cached_property

from utils import Log

from utils_future.WWW import WWW

log = Log("AbstractDocExtendedDataMixin")


class AbstractDocExtendedDataMixin:
    T_TIMEOUT_PDF_DOWNLOAD = 120

    @cached_property
    def dir_doc_extended_without_base(self) -> str:
        return os.path.join(
            self.get_dir_docs_root(),
            self.decade,
            self.year,
            self.doc_id,
        )

    @classmethod
    def get_dir_doc_extended_root(cls) -> str:
        dir_metadata = os.path.basename(os.getcwd())
        return os.path.join(
            "..",
            f"{dir_metadata}_data",
        )

    @cached_property
    def dir_doc_extended(self) -> str:
        return os.path.join(
            self.get_dir_doc_extended_root(),
            self.dir_doc_extended_without_base,
        )

    def __copy_metadata__(self):
        shutil.copytree(
            self.dir_doc, self.dir_doc_extended, dirs_exist_ok=True
        )
        log.info(f"Copied metadata to {self.dir_doc_extended}")

    @cached_property
    def pdf_path(self) -> str:
        return os.path.join(self.dir_doc_extended, "en.pdf")

    @property
    def has_pdf(self) -> bool:
        return os.path.exists(self.pdf_path)

    def __download_pdf__(self):
        WWW(self.remote_data_url).download_binary(self.pdf_path)

    def scrape_extended_data(self):
        if not os.path.exists(self.dir_doc_extended):
            os.makedirs(self.dir_doc_extended)
            self.__copy_metadata__()
        if not self.has_pdf:
            self.__download_pdf__()

    @cached_property
    def remote_data_url(self) -> str:
        raise NotImplementedError

    @classmethod
    def get_total_file_size(cls):
        # get size of get_dir_doc_extended_root
        total_size = 0
        for dirpath, _, filenames in os.walk(cls.get_dir_doc_extended_root()):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
