import os

from utils import Log

from appeals import AppealsDoc

log = Log("appeals_pipeline")


def update_data_repo():
    log.debug("Updating data repo...")
    os.system(
        " && ".join(
            [
                "cd ../lk_judiciary_appeals_court_data",
                "git reset --hard HEAD",
                "git clean -fd",
                "git pull origin data",
                "cd -",
            ]
        )
    )


if __name__ == "__main__":
    update_data_repo()
    AppealsDoc.run_pipeline()
