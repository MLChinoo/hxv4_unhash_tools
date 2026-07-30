"""
从scenelist.csv中获取cg缩略图thum
此来源可以获取到影片movie缩略图movthum(opthum/edthum)
"""

import csv

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_scenelist_csv")
def collect(self: PlainDict, scenelist_csv_filepath, file_encoding: str = "utf-16le"):
    with open(scenelist_csv_filepath, mode="r", encoding=file_encoding) as f:
        scenelist_csv = csv.reader(f)
        for row in scenelist_csv:
            if len(row) == 0:
                continue
            header = row[0].replace("\ufeff", "")  # remove bom
            if header.startswith("#") or ":" in header:
                continue
            filenames = row[0].split("|")
            for filename in filenames:
                for locale in ("", "_jp", "_en", "_cn", "_tw"):
                    self.filename_plaintexts.update([
                        f"{filename}{locale}.jpg",
                        f"{filename}{locale}.png",
                        f"{filename}{locale}.psb",
                        f"{filename}{locale}.tlg",
                        
                        f"{filename}{locale}_censored.jpg",
                        f"{filename}{locale}_censored.png",
                        f"{filename}{locale}_censored.psb",
                        f"{filename}{locale}_censored.tlg"
                    ])
    return self
