"""
从soundlist.csv文件中获取bgm文件名
"""

import csv

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_soundlist_csv")
def collect(self: PlainDict, soundlist_csv_filepath, file_encoding: str = "utf-16le"):
    with open(soundlist_csv_filepath, mode="r", encoding=file_encoding) as f:
        soundlist_csv = csv.reader(f)
        for row in soundlist_csv:
            if len(row) > 0:
                header = row[0]
                if not header.startswith("#"):
                    self.filename_plaintexts.update((
                        f"{header}.opus",
                        f"{header}.opus.sli",
                        f"{header}.ogg",
                        f"{header}.ogg.sli",
                        f"{header}.mchx",
                        f"{header}.mchx.sli"
                    ))
    return self
