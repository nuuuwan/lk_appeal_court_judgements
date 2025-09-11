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
            print(asdict(first_doc))
            self.assertEqual(
                asdict(first_doc),
                {
                    "num": "C.A. WRIT 388/2020",
                    "date_str": "2021-01-26",
                    "description": "K.M.S. Bandara Vs Air Marshal D.L.S. Dias, Commander of the Air Force and Others - before Hon. Sobhitha Rajakaruna, J",  # noqa: E501
                    "url_pdf": "https://courtofappeal.lk/?melsta_doc_download=1&doc_id=90b94e44-e1d2-478a-a1ac-23379f1beb6f&filename=c.a%20writ%20%20388-2019.pdf.pdf",  # noqa: E501
                    "parties": "K.M.S. Bandara Vs Air Marshal D.L.S. Dias, Commander of the Air Force and Others -",  # noqa: E501
                    "judgement_by": "Hon. Sobhitha Rajakaruna, J",
                    "keywords": "",
                    "legistation": "",
                },
            )

        # # hack
        # from appeals import AppealsDataPage

        # for doc in doc_list:
        #     doc.description = AppealsDataPage.clean_text(doc.description)
        #     doc.parties = AppealsDataPage.clean_text(doc.parties)
        #     doc.judgement_by = AppealsDataPage.clean_text(doc.judgement_by)
        #     doc.keywords = AppealsDataPage.clean_text(doc.keywords)
        #     doc.legistation = AppealsDataPage.clean_text(doc.legistation)
        #     doc.write()
