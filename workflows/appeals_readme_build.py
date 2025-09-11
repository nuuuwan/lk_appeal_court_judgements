from appeals import AppealsDoc
from pdf_scraper import ReadMe

if __name__ == "__main__":
    readme = ReadMe(AppealsDoc)
    readme.build()
