import os
import shutil
from pathlib import Path

from utils import JSONFile, Log

log = Log("cleanup_errors")


def cleanup_metadata_with_missing_url_metadata(do_delete):
    log.info("cleanup_metadata_with_missing_url_metadata")
    n_delete = 0
    for json_path in Path("data").rglob("doc.json"):
        data = JSONFile(json_path).read()
        if "url_metadata" not in data:
            dir_path = os.path.dirname(json_path)
            n_delete += 1
            if do_delete:
                log.warning(f"Removing directory {dir_path}")
                shutil.rmtree(dir_path)
    log.info(f"Found {n_delete:,} docs with missing metadata")


def cleanup_extended_data_with_missing_url_metadata(do_delete):
    log.info("cleanup_extended_data_with_missing_url_metadata")
    n_delete = 0
    for json_path in Path("../lk_judiciary_appeals_court_data/data").rglob(
        "doc.json"
    ):
        data = JSONFile(json_path).read()
        if "url_metadata" not in data:
            dir_path = os.path.dirname(json_path)
            n_delete += 1
            if do_delete:
                log.warning(f"Removing directory {dir_path}")
                shutil.rmtree(dir_path)
    log.info(f"Found {n_delete:,} extended docs with missing metadata")


def cleanup_extended_data_with_wrong_id(do_delete):
    log.info("cleanup_extended_data_with_wrong_id")
    n_delete = 0
    for json_path in Path("../lk_judiciary_appeals_court_data/data").rglob(
        "doc.json"
    ):
        if "--8-" in str(json_path):
            dir_path = os.path.dirname(json_path)
            n_delete += 1
            if do_delete:
                log.warning(f"Removing directory {dir_path}")
                shutil.rmtree(dir_path)
    log.info(f"Found {n_delete:,} extended docs with wrong_id")


def main(do_delete=False):
    cleanup_metadata_with_missing_url_metadata(do_delete)
    cleanup_extended_data_with_missing_url_metadata(do_delete)
    cleanup_extended_data_with_wrong_id(do_delete)


if __name__ == "__main__":
    main(True)
