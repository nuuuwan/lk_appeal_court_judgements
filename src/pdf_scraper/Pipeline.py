import time

from utils import Log

from pdf_scraper.AbstractHomePage import AbstractHomePage

log = Log("Pipeline")


class Pipeline:
    class DEFAULT:
        MAX_DT = 10

    def __init__(self, home_page_class: type[AbstractHomePage]):
        self.home_page_class = home_page_class

    @staticmethod
    def log_processed_doc(docs, dt):
        n_docs = len(docs)
        log.info(f"🛑 Processed {n_docs} docs in {dt:,.1f}s")

    def run(self, max_dt: int = None):
        max_dt = max_dt or Pipeline.DEFAULT.MAX_DT
        log.debug(f"{max_dt=}s")
        home_page = self.home_page_class()
        t_start = time.time()
        docs = []
        dt = 0
        for data_page in home_page.gen_data_pages():
            for doc in data_page.gen_docs():
                doc.write()
                docs.append(doc)
                dt = time.time() - t_start
            if dt > max_dt:
                Pipeline.log_processed_doc(docs, dt)
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        Pipeline.log_processed_doc(docs, dt)
        log.info("🛑 All docs processed.")
