"""
从给定的uipsd文件夹下查找已命名的.pbd和.tlg文件，并获取其多语言变体文件名。
建议和scan_uipsd_pbds()一起多次循环使用来提升覆盖率。
"""

import re
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="scan_uipsd_multi_lang")
def collect(self: PlainDict, uipsd_dir: str):
    uipsd_bases = set()
    for child in Path(uipsd_dir).rglob("*"):
        if child.is_file():
            match = re.match(r"^(.+?)(?:_(?:jp|en|cn|tw))?(?:__(?:bg\d+|pack))?\.(?:pbd|tlg)$", child.name)
            if match:
                uipsd_bases.add(match.group(1))

    suffixes = [
        ".pbd",
        "__bg0.tlg",
        "__bg1.tlg",
        "__bg2.tlg",
        "__pack.tlg",
        "_jp.pbd",
        "_jp__pack.tlg",
        "_en.pbd",
        "_en__pack.tlg",
        "_cn.pbd",
        "_cn__pack.tlg",
        "_tw.pbd",
        "_tw__pack.tlg"
    ]
    for uipsd_base in uipsd_bases:
        for suffix in suffixes:
            self.filename_plaintexts.add(f"{uipsd_base}{suffix}")
    return self
