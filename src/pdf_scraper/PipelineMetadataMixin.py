import time

from utils import Log

from pdf_scraper.Pipeline import Pipeline

log = Log("PipelineMetadataMixin")


class PipelineMetadataMixin:

    @staticmethod
    def __log_processed_doc__(docs, dt):
        n_docs = len(docs)
        log.info(f"🛑 Processed {n_docs:,} docs in {dt:,.1f}s")

    def __scrape_metadata__(self, max_dt, t_start):
        home_page = self.home_page_class()
        docs = []
        dt = 0
        for data_page in home_page.gen_data_pages():
            for doc in data_page.gen_docs():
                doc.write()
                docs.append(doc)
                dt = time.time() - t_start
            if dt > max_dt:
                Pipeline.__log_processed_doc__(docs, dt)
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        Pipeline.__log_processed_doc__(docs, dt)
        log.info("🛑 All docs processed.")
