from utils import Log

from appeals import AppealsDoc

log = Log("appeals_pipeline")


if __name__ == "__main__":
    AppealsDoc.run_pipeline()
