from appeals import AppealsDoc, AppealsHomePage
from pdf_scraper import ReadMe

if __name__ == "__main__":
    readme = ReadMe(AppealsHomePage, AppealsDoc)
    readme.build()
