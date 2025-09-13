from utils import File, Log

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def __init__(self, home_page_class, doc_class):
        self.home_page_class = home_page_class
        self.doc_class = doc_class

    @property
    def lines_for_docs(self):
        lines = []

        for (
            year,
            doc_list_for_year,
        ) in self.doc_class.year_to_month_to_doc_list().items():
            lines.extend([f"## {year}", ""])
            for year_month, doc_list_for_month in doc_list_for_year.items():
                lines.extend([f"### {year_month}", ""])
                for doc in doc_list_for_month:
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
    def lines_for_summary(self) -> list[str]:
        doc_list = self.doc_class.list_all()
        n_docs = len(doc_list)
        date_strs = [doc.date_str for doc in doc_list]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)
        url = self.home_page_class().url
        n_docs_with_pdf = sum(1 for doc in doc_list if doc.has_pdf)
        p_docs_with_pdf = n_docs_with_pdf / n_docs
        return [
            f"**{n_docs:,}** documents"
            + f" from **{date_str_min}** to **{date_str_max}**"
            + " downloaded from"
            + f" [{url}]({url}).",
            "",
            "PDFs downloaded for"
            + f" {n_docs_with_pdf:,} ({p_docs_with_pdf:.1%}) documents.",
            "",
        ]

    @property
    def lines_for_header(self) -> list[str]:
        return [f"# {self.doc_class.doc_class_pretty_label()}", ""]

    @property
    def lines(self) -> list[str]:
        return (
            self.lines_for_header
            + self.lines_for_summary
            + self.lines_for_docs
        )

    def build(self):
        File(self.PATH).write("\n".join(self.lines))
        log.info(f"Wrote {self.PATH}")
