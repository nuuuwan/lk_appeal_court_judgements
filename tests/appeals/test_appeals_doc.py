import unittest
from dataclasses import asdict

from appeals import AppealsDoc


class TestCase(unittest.TestCase):

    def test_list_all(self):
        doc_list = AppealsDoc.list_all()
        self.assertIsInstance(doc_list, list)
        if doc_list:
            self.assertGreater(len(doc_list), 10)
            first_doc = doc_list[-1]
            print(
                asdict(first_doc),
            )
            self.assertEqual(
                asdict(first_doc),
                {
                    "num": "C.A. WRIT 388/2020",
                    "date_str": "2021-01-26",
                    "description": "K.M.S. Bandara Vs Air Marshal D.L.S. Dias,  Commander of the Air Force and Others - before Hon. Sobhitha Rajakaruna, J",
                    "url_pdf": "/?melsta_doc_download=1&doc_id=90b94e44-e1d2-478a-a1ac-23379f1beb6f&filename=c.a writ  388-2019.pdf.pdf",
                    "parties": "K.M.S. Bandara Vs Air Marshal D.L.S. Dias,  Commander of the Air Force and Others -",
                    "judgement_by": "Hon. Sobhitha Rajakaruna, J",
                    "keywords": "",
                    "legistation": "",
                },
            )

        # hack
        # https://courtofappeal.lk/?page_id=10834

        for doc in doc_list:
            if not doc.url_pdf.startswith("https://courtofappeal.lk"):
                doc.url_pdf = "https://courtofappeal.lk" + doc.url_pdf
                doc.write()
