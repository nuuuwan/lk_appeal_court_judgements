import re
from functools import cached_property
from typing import Generator
from urllib.parse import quote

from utils import Log

from appeals.AppealsDataPage import AppealsDataPage
from appeals.AppealsDoc import AppealsDoc

log = Log("AppealsOldDataPage")


class AppealsOldDataPage(AppealsDataPage):

    def __parse_title__(self, title) -> tuple:
        title = title.replace("CA ", "CA").replace("CA. ", "CA.")
        title = title.replace(" / ", "/")
        title = title.replace("-", "-")
        tokens = title.split("/")

        end_num_and_rest = tokens[-1]
        start_num = "/".join(tokens[:-1])
        if " " in end_num_and_rest:
            end_num, parties_and_judgement_part = end_num_and_rest.split(
                " ", 1
            )
        else:
            end_num = end_num_and_rest
            parties_and_judgement_part = ""

        num = start_num + "/" + end_num

        if parties_and_judgement_part:
            if " - " in parties_and_judgement_part:
                tokens2 = parties_and_judgement_part.split("-")
                judgement_by = tokens2[-1]
                parties = "-".join(tokens2[0:-1]).strip()
            else:
                if "Hon." in parties_and_judgement_part:
                    parties = ""
                    judgement_by = parties_and_judgement_part
                else:
                    parties = parties_and_judgement_part.strip()
                    judgement_by = ""

        else:
            parties = ""
            judgement_by = ""

        keywords, legistations = "", ""
        return num, parties, judgement_by, keywords, legistations

    def __parse_tr__(self, tr) -> AppealsDoc:
        tds = tr.find_all("td")
        text_list = [self.clean_text(td.get_text()) for td in tds]

        date_str = text_list[0]
        if date_str in ["-"]:
            return None
        assert len(date_str) == 10, date_str

        url_pdf = self.__parse_url__(tds[3].find("a")["href"])
        num, parties, judgement_by, keywords, legistation = (
            self.__parse_title__(text_list[1])
        )

        description = f"{parties} before {judgement_by}"

        return AppealsDoc(
            # from AbstractDoc
            num=num,
            date_str=date_str,
            description=description,
            url_pdf=url_pdf,
            # specific
            parties=parties,
            judgement_by=judgement_by,
            keywords=keywords,
            legistation=legistation,
        )

    def gen_docs(self) -> Generator[AppealsDoc, None, None]:
        table = self.soup.find("table")
        if not table:
            return
        tbody = table.find("tbody")
        for tr in tbody.find_all("tr"):
            doc = self.__parse_tr__(tr)
            if doc:
                yield doc
