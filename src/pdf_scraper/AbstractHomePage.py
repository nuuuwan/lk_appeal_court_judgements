from abc import ABC, Generator, abstractmethod

from pdf_scraper.AbstractDataPage import AbstractDataPage
from utils_future import WebPage


class AbstractHomePage(WebPage, ABC):

    @abstractmethod
    def gen_data_pages(self) -> Generator[AbstractDataPage]:
        pass
