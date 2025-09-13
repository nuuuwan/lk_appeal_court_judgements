import time

from utils import Log

log = Log("PipelineExtendedDataMixin")


class PipelineExtendedDataMixin:
    def __scrape_extended_data__(self, max_dt, t_start):
        for doc in self.doc_class.list_all():
            doc.scrape_extended_data()
            dt = time.time() - t_start
            if dt > max_dt:
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        log.info("🛑 All extended data scraped.")
