import unittest

from pdf_scraper import AbstractDoc


class TestCase(unittest.TestCase):
    def test_list_all(self):
        doc_list = AbstractDoc.list_all()
        self.assertIsInstance(doc_list, list)
        if doc_list:
            self.assertGreater(len(doc_list), 10)
            first_doc = doc_list[0]
            self.assertEqual(len(first_doc.date_str), 10)
