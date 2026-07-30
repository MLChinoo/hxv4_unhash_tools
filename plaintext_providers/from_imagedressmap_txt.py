"""
从imagedressmap.txt文件中获取stand文件名
"""

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_imagedressmap_txt")
def collect(self: PlainDict, imagedressmap_txt_filepath, file_encoding: str):
    with open(imagedressmap_txt_filepath, mode="r", encoding=file_encoding) as f:
        content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            stand_name = parts[0].strip()
            if stand_name:
                if not stand_name.endswith(".stand"):
                    stand_name = f"{stand_name}.stand"
                self.filename_plaintexts.add(stand_name)
    return self
