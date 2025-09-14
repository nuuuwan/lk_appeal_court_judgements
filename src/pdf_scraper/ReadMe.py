from utils import File, Log

from pdf_scraper.ChartDocsByYear import ChartDocsByYear
from utils_future import Markdown

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"
    N_LATEST = 20

    def __init__(self, home_page_class, doc_class):
        self.home_page_class = home_page_class
        self.doc_class = doc_class

    @property
    def lines_for_latest_docs(self):
        lines = [f"## {self.N_LATEST} Latest documents", ""]
        for doc in self.doc_class.list_all()[: self.N_LATEST]:
            line = "- " + " | ".join(
                [
                    doc.date_str,
                    f"`{doc.num}`",
                    doc.description,
                    f"[data]({doc.remote_data_url})",
                ]
            )
            lines.append(line)
        lines.append("")
        return lines

    @property
    def lines_chart_docs_by_year(self) -> list[str]:
        chart = ChartDocsByYear(self.doc_class)
        chart.build()
        return [
            "## Documents by year",
            "",
            f"![Documents by year]({chart.image_path})",
            "",
        ]

    @property
    def lines_for_summary(self) -> list[str]:
        doc_list = self.doc_class.list_all()
        n_docs = len(doc_list)
        log.debug(f"{n_docs=}")
        date_strs = [doc.date_str for doc in doc_list]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)
        url = self.home_page_class().url
        n_docs_with_pdf = sum(1 for doc in doc_list if doc.has_pdf)
        log.debug(f"{n_docs_with_pdf=}")
        file_size_g = self.doc_class.get_total_file_size() / 1_000_000_000
        log.debug(f"{file_size_g=:.1f}")

        d_list = [
            dict(
                source=url,
                date_min=date_str_min,
                date_max=date_str_max,
                n_docs=f"{n_docs:,}",
                n_docs_with_pdf=f"{n_docs_with_pdf:,}",
                dataset_size=f"{file_size_g:.1f}GB",
            ),
        ]
        return (
            [
                "## Data Summary",
                "",
            ]
            + Markdown.table(d_list)
            + [""]
        )

    @property
    def lines_for_header(self) -> list[str]:
        return [f"# {self.doc_class.doc_class_pretty_label()}", ""]

    @property
    def lines(self) -> list[str]:
        return (
            self.lines_for_header
            + self.lines_for_summary
            + self.lines_chart_docs_by_year
            + self.lines_for_latest_docs
        )

    def build(self):
        File(self.PATH).write("\n".join(self.lines))
        log.info(f"Wrote {self.PATH}")
