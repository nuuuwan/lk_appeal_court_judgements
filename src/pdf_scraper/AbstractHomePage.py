from abc import ABC, abstractmethod
from typing import Generator

from pdf_scraper.AbstractDataPage import AbstractDataPage
from utils_future import WebPage


class AbstractHomePage(WebPage, ABC):

    @abstractmethod
    def gen_data_pages(self) -> Generator[AbstractDataPage, None, None]:
        pass
