"""
从imageevalmap.csv文件中获取图片映射文件名
"""

import csv

from plaintext_providers import register


@register(name="from_imageevalmap_csv")
def collect(self, imageevalmap_csv_filepath, file_encoding: str = "utf-16le"):
    count = 0
    with open(imageevalmap_csv_filepath, mode="r", encoding=file_encoding) as f:
        imageevalmap_csv = csv.reader(f)
        for row in imageevalmap_csv:
            if not row:
                continue

            header = row[0].replace("\ufeff", "").strip()
            if header.startswith("#") or not header:
                continue

            for field in row[:2]:
                image_name = field.strip()
                if image_name and not image_name.startswith("&") and not image_name.startswith("#"):
                    for extension in (".pimg", ".tlg", ".png", ".psb"):
                        self.filename_plaintexts.update([
                            f"{image_name}{extension}",
                            f"{image_name}_censored{extension}"
                        ])
                    count += 1

    if count > 0:
        print(f"[imageevalmap] 提取了 {count} 个图片名")
    return self
