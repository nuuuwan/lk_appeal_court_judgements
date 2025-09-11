from utils import File, Log

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def __init__(self, doc_class):
        self.doc_class = doc_class

    @property
    def lines_for_docs(self):
        doc_list = self.doc_class.list_all()
        lines = []
        for doc in doc_list:
            line = f"- {
                doc.date_str} | {
                doc.num} | {
                doc.description} | [pdf]({
                doc.url_pdf})"
            lines.append(line)
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
