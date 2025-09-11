import sys

from appeals import AppealsDoc, AppealsHomePage, AppealsPipeline
from pdf_scraper import ReadMe

if __name__ == "__main__":
    AppealsPipeline().run(
        max_dt=int(sys.argv[1]) if len(sys.argv) > 1 else None
    )
    ReadMe(AppealsHomePage, AppealsDoc).build()
