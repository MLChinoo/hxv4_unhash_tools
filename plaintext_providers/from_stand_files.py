"""
从给定的fgimage目录下查找人物.stand文件，并获取.pbd文件名和.sinfo文件名
需要先扫描一遍psb来获取.stand文件
"""

import re
from pathlib import Path

from plaintext_providers import register


@register(name="from_stand_files")
def collect(self, fgimage_dir, file_encoding: str = "utf-16le"):
    count = 0
    for child in Path(fgimage_dir).rglob("*.stand"):
        if child.is_file():
            with open(child, mode="r", encoding=file_encoding) as cf:
                # TODO: refactor using TjsParser
                filenames = re.findall(r"filename:'([^']+)'", cf.read())
                for filename in filenames:
                    self.filename_plaintexts.update([
                        f"{filename}.pbd",
                        f"{filename}.sinfo",
                        f"{filename}_0.pbd",
                        f"{filename}_0.sinfo",
                        f"{filename}_info.txt"
                    ])
                    count += 1
    if count > 0:
        print(f"[stand] 提取了 {count} 个立绘条目")
    return self
