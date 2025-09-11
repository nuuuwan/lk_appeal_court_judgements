from abc import ABC, abstractmethod

from pdf_scraper.AbstractDataPage import AbstractDataPage
from utils_future import WebPage


class AbstractHomePage(WebPage, ABC):

    @abstractmethod
    def get_data_pages(self) -> list[AbstractDataPage]:
        pass
