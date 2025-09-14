import tempfile

import pymupdf
from utils import Log

log = Log("PDFCompressMixin")


class PDFCompressMixin:
    DPI_TARGET = 75
    QUALITY = 25

    @staticmethod
    def __compress_with_pymupdf__(input_path, output_path):
        assert input_path != output_path
        doc = pymupdf.open(input_path)

        doc.rewrite_images(
            dpi_target=PDFCompressMixin.DPI_TARGET,
            dpi_threshold=PDFCompressMixin.DPI_TARGET + 1,
            quality=PDFCompressMixin.QUALITY,
        )
        doc.ez_save(output_path)

    def compress(self, output_pdf_path):
        self.__compress_with_pymupdf__(self.path, output_pdf_path)
        output_pdf_file = self.__class__(output_pdf_path)
        log.debug(f"Compressed {self} to {output_pdf_file}")
        return output_pdf_file

    @staticmethod
    def temp_pdf_path():
        return tempfile.mktemp(suffix=".pdf")
