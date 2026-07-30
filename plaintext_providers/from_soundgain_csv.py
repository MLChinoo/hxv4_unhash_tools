"""
从soundgain.csv文件中获取音效区分文件名
"""

import csv

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_soundgain_csv")
def collect(self: PlainDict, soundgain_csv_filepath, file_encoding: str):
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
    return self
