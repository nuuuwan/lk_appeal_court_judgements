import os

from utils import Log

from appeals import AppealsDoc, AppealsHomePage
from pdf_scraper import ReadMe

log = Log("appeals_readme_build")


def update_data_repo():
    log.debug("Updating data repo...")
    os.system(
        " && ".join(
            [
                "cd ../lk_judiciary_appeals_court_data",
                "git pull origin data",
                "cd -",
            ]
        )
    )


def main():
    update_data_repo()
    ReadMe(AppealsHomePage, AppealsDoc).build()


if __name__ == "__main__":
    main()
