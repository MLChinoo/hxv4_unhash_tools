"""
从scenelist.csv中获取cg缩略图thum
此来源可以获取到影片movie缩略图movthum
"""

import csv

from plaintext_providers import register


@register(name="from_scenelist_csv")
def collect(self, scenelist_csv_filepath):
    with open(scenelist_csv_filepath, mode="r", encoding="utf-16le") as f:
        scenelist_csv = csv.reader(f)
        for row in scenelist_csv:
            if len(row) > 0:
                header = row[0].replace("\ufeff", "")  # remove bom
                if not header.startswith("#"):
                    if ":" in header:
                        print(f"bad cg_filename, ignored: {header} in {scenelist_csv_filepath}")
                        continue
                    filenames = row[0].split("|")
                    for filename in filenames:
                        self.filename_plaintexts.update([
                            f"{filename}.jpg",
                            f"{filename}.png",
                            f"{filename}_censored.jpg",
                            f"{filename}_censored.png",
                            f"{filename}.psb",
                            f"{filename}_censored.psb",
                        ])
    return self
