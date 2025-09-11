from abc import ABC, abstractmethod
from typing import Generator

from pdf_scraper.AbstractDoc import AbstractDoc
from utils_future import WebPage


class AbstractDataPage(WebPage, ABC):

    @abstractmethod
    def gen_docs(self) -> Generator[AbstractDoc, None, None]:
        pass
