"""
从scenelist.csv中获取cg缩略图thum
此来源可以获取到影片movie缩略图movthum
"""

import csv

from plaintext_providers import register


@register(name="from_scenelist_csv")
def collect(self, scenelist_csv_filepath, file_encoding: str = "utf-16le"):
    count = 0
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
                self.filename_plaintexts.update([
                    f"{filename}.jpg",
                    f"{filename}.png",
                    f"{filename}.psb",
                    f"{filename}.tlg",
                    
                    f"{filename}_censored.jpg",
                    f"{filename}_censored.png",
                    f"{filename}_censored.psb",
                    f"{filename}_censored.tlg"
                ])
            count += 1
    print(f"[scenelist.csv] 提取了 {count} 个场景条目")
    return self
