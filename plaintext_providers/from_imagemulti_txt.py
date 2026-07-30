"""
从imagemulti.txt文件中获取fgimage立绘文件名
"""

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_imagemulti_txt")
def collect(self: PlainDict, imagemulti_txt_filepath, file_encoding: str):
    with open(imagemulti_txt_filepath, mode="r", encoding=file_encoding) as f:
        content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            for part in parts:
                part = part.strip()
                if ":" in part:
                    part = part.split(":", 1)[1].strip()
                if not part:
                    continue
                for extension in (".pbd", ".sinfo", ".pimg", ".stand"):
                    self.filename_plaintexts.add(f"{part}{extension}")
    return self
