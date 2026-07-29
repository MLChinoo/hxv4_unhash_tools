"""
从soundlist.csv文件中获取bgm文件名
"""

import csv

from plaintext_providers import register


@register(name="from_soundlist_csv")
def collect(self, soundlist_csv_filepath):
    with open(soundlist_csv_filepath, mode="r", encoding="utf-16le") as f:
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
