from appeals import AppealsDoc, AppealsHomePage
from pdf_scraper import ReadMe

if __name__ == "__main__":
    ReadMe(AppealsHomePage, AppealsDoc).build()
