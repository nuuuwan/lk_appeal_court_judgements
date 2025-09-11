import time

from utils import Log

from pdf_scraper.AbstractHomePage import AbstractHomePage

log = Log("Pipeline")


class Pipeline:
    class DEFAULT:
        MAX_DT = 10

    def __init__(self, home_page_class: type[AbstractHomePage]):
        self.home_page_class = home_page_class

    def run(self, max_dt: int = None):
        max_dt = max_dt or Pipeline.DEFAULT.MAX_DT
        home_page = self.home_page_class()
        t_start = time.time()
        for data_page in home_page.gen_data_pages():
            for doc in data_page.gen_docs():
                doc.write()
                dt = time.time() - t_start
                if dt > max_dt:
                    log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                    return

        log.info("🛑 All docs processed.")
