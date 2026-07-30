"""
从systrans.ini文件中获取转场规则文件名
"""

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_systrans_ini")
def collect(self: PlainDict, systrans_ini_filepath, file_encoding: str):
    rules = set()
    with open(systrans_ini_filepath, mode="r", encoding=file_encoding) as f:
        content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            right_hand_side = line.split("=", 1)[1].strip()
            if right_hand_side.startswith("@") or right_hand_side.startswith("0:&"):
                continue
            for part in right_hand_side.split(":"):
                part = part.strip()
                if part and not part.isdigit() and not part.startswith("@"):
                    rules.add(part)

    for rule in rules:
        for extension in (".png", ".pimg", ".tlg", ".psb"):
            self.filename_plaintexts.add(f"{rule}{extension}")
    return self
