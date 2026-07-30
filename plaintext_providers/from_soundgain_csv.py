"""
从soundgain.csv文件中获取音效区分文件名
"""

import csv

from plaintext_providers import register


@register(name="from_soundgain_csv")
def collect(self, soundgain_csv_filepath, file_encoding: str):
    count = 0
    with open(soundgain_csv_filepath, mode="r", encoding=file_encoding) as f:
        soundgain_csv = csv.reader(f)
        for row in soundgain_csv:
            if not row:
                continue
            sound_name = row[0].replace("\ufeff", "").strip()
            if sound_name.startswith("#") or not sound_name:
                continue
            for extension in (".ogg", ".ogg.sli"):
                self.filename_plaintexts.add(f"{sound_name}{extension}")
            count += 1

    if count > 0:
        print(f"[soundgain] 提取了 {count} 个音效区分名")
    return self
