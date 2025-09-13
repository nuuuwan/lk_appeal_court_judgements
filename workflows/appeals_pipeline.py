from appeals import AppealsDoc, AppealsHomePage, AppealsPipeline
from pdf_scraper import ReadMe

if __name__ == "__main__":
    AppealsPipeline().run()
    ReadMe(AppealsHomePage, AppealsDoc).build()
