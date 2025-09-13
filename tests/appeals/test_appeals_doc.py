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
                list(asdict(first_doc).keys()),
            )
            self.assertEqual(
                list(asdict(first_doc).keys()),
                [
                    "num",
                    "date_str",
                    "description",
                    "url_pdf",
                    "parties",
                    "judgement_by",
                    "keywords",
                    "legistation",
                ],
            )
