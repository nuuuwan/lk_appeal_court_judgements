from abc import ABC, Generator, abstractmethod

from pdf_scraper.AbstractDoc import AbstractDoc
from utils_future import WebPage


class AbstractDataPage(WebPage, ABC):

    @abstractmethod
    def gen_docs(self) -> Generator[AbstractDoc]:
        pass
