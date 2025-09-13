from appeals.AppealsDoc import AppealsDoc
from appeals.AppealsHomePage import AppealsHomePage
from pdf_scraper import Pipeline


class AppealsPipeline(Pipeline):
    def __init__(self):
        super().__init__(AppealsHomePage, AppealsDoc)
