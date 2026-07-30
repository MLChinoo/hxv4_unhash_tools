"""
从imagediffmap.csv文件中获取cg文件名evimage
"""

import csv

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_imagediffmap_csv")
def collect(self: PlainDict, imagediffmap_csv_filepath, file_encoding: str = "utf-16le"):
    with open(imagediffmap_csv_filepath, mode="r", encoding=file_encoding) as f:
        imagediffmap_csv = csv.reader(f)
        for row in imagediffmap_csv:
            if len(row) < 2:
                continue
            header = row[0].replace("\ufeff", "")  # remove bom
            if header.startswith("#"):
                continue
            filename = row[1]
            if "." in filename:
                if filename.count(".") > 1:
                    print(f"warning: multiple extensions file - {filename}")
                names, extension = filename.split(".", 1)
                names = names.split("|")
                for name in names:
                    self.filename_plaintexts.add(
                        f"{name}.{extension}"
                    )
            else:
                self.filename_plaintexts.update([
                    f"{filename}.pimg",
                    f"{filename}_censored.pimg",
                    f"{filename}.psb",
                    f"{filename}_censored.psb",
                    f"{filename}.tlg",
                    f"{filename}_censored.tlg",
                    
                    f"savethum_{filename}.jpg",
                    f"savethum_{filename}.png",
                    f"savethum_{filename}.psb",
                    f"savethum_{filename}.tlg"
                ])
    return self
