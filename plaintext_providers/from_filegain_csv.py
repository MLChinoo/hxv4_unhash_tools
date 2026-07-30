"""
从filegain.csv文件中获取音效和BGM文件名
"""

import csv

from plaintext_providers import register


@register(name="from_filegain_csv")
def collect(self, filegain_csv_filepath, file_encoding: str):
    count = 0
    with open(filegain_csv_filepath, mode="r", encoding=file_encoding) as f:
        filegain_csv = csv.reader(f)
        for row in filegain_csv:
            if not row:
                continue
            sound_name = row[0].replace("\ufeff", "").strip()
            if sound_name.startswith("#") or not sound_name:
                continue
            for extension in (".ogg", ".ogg.sli", ".opus", ".opus.sli", ".mchx", ".mchx.sli"):
                self.filename_plaintexts.add(f"{sound_name}{extension}")
            count += 1

    if count > 0:
        print(f"[filegain] 提取了 {count} 个音效/BGM 名")
    return self
