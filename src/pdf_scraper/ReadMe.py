from utils import File, Log

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def __init__(self, doc_class):
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
                            f"[metadata]({doc.json_path})",
                            f"[pdf]({doc.url_pdf})",
                        ]
                    )
                    lines.append(line)
                lines.append("")

        return lines

    @property
    def lines(self) -> list[str]:
        return (
            [f"# {self.doc_class.doc_class_label()}"]
            + [""]
            + self.lines_for_docs
        )

    def build(self):
        File(self.PATH).write("\n".join(self.lines))
        log.info(f"Wrote {self.PATH}")
