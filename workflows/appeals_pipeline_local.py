import os

from utils import Log

from appeals import AppealsDoc

log = Log("appeals_pipeline_local")


def extended_data_repo_pull():
    log.debug("extended_data_repo_pull...")
    os.system(
        " && ".join(
            [
                "cd ../lk_judiciary_appeals_court_data",
                "git reset --hard HEAD",
                "git clean -fd",
                "git pull origin data --rebase",
                "cd -",
            ]
        )
    )


def extended_data_repo_push():
    log.debug("extended_data_repo_push...")
    os.system(
        " && ".join(
            [
                "cd ../lk_judiciary_appeals_court_data",
                "git add .",
                "git commit -m '👶🏾 [appeals_pipeline_local]'",
                "git pull origin data --rebase",
                "git push origin data",
                "cd -",
            ]
        )
    )


def data_repo_push():
    log.debug("data_repo_push...")
    os.system(
        " && ".join(
            [
                "git add .",
                "git commit -m '👶🏾 [appeals_pipeline_local]'",
                "git push origin data",
                "cd -",
            ]
        )
    )


if __name__ == "__main__":
    extended_data_repo_pull()
    AppealsDoc.run_pipeline()
    extended_data_repo_push()
    data_repo_push()
