"""
从给定的fgimage目录下查找人物.stand文件，并获取.pbd文件名和.sinfo文件名
需要先扫描一遍psb来获取.stand文件
"""

import re
from pathlib import Path

from plaintext_providers import register


@register(name="from_stand_files")
def collect(self, fgimage_dir):
    for child in Path(fgimage_dir).rglob("*"):
        if all((child.is_file(), child.suffix == ".stand")):
            with open(child, mode="r", encoding="utf-16le") as cf:
                filenames = re.findall(r"filename:'([^']+)'", cf.read())
                for filename in filenames:
                    self.filename_plaintexts.update([
                        f"{filename}.pbd",
                        f"{filename}.sinfo",
                        f"{filename}_0.pbd",
                        f"{filename}_0.sinfo"
                    ])
    return self
