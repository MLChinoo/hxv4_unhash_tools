"""
从给定的fgimage目录下查找人物.stand文件，并获取.pbd文件名和.sinfo文件名
需要先scan_psb_and_decompile()扫描一遍psb来获取.stand文件
"""

import re
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="scan_fgimage_stands")
def collect(self: PlainDict, fgimage_dir, file_encoding: str = "utf-16le"):
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
    return self
