"""
从savelist.csv文件中获取存档图片savethum
"""

import csv

from plaintext_providers import register


@register(name="from_savelist_csv")
def collect(self, savelist_csv_filepath, file_encoding: str = "utf-16le"):
    count = 0
    with open(savelist_csv_filepath, mode="r", encoding=file_encoding) as f:
        savelist_csv = csv.reader(f)
        for row in savelist_csv:
            if len(row) == 0:
                continue
            header = row[0].replace("\ufeff", "")  # remove bom
            if header.startswith("#"):
                continue
            filename = row[0]
            self.filename_plaintexts.update([
                f"{filename}.jpg",
                f"{filename}.png",
                f"{filename}.psb",
                f'{filename.replace("savethum_", "thum_")}.jpg',
                f'{filename.replace("savethum_", "thum_")}.png',
                f'{filename.replace("savethum_", "thum_")}.psb'
            ])
            count += 1
    print(f"[savelist.csv] 提取了 {count} 个存档条目")
    return self
