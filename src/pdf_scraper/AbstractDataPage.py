from abc import ABC, abstractmethod

from utils_future import WebPage


class AbstractDataPage(WebPage, ABC):

    @abstractmethod
    def get_docs(self) -> list[str]:
        pass
