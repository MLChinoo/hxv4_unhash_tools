"""
从给定目录中已命名的tjs文件获取字符串中的文件名引用
"""

import re
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="scan_tjs_scripts_re")
def collect(self: PlainDict, tjs_dir: str, file_encoding: str):
    seen = set()
    pattern = re.compile(r'["\']([^"\'\s]+\.(?:tjs|ks|ini|csv|txt|png|jpg|tlg|pimg|ogg|mp4|wmv|psb|pbd|stand|sinfo|mtn|stage|toml))["\']')
    for child in Path(tjs_dir).rglob("*"):
        if not child.is_file() or not child.name.endswith(".tjs"):
            continue
        with open(child, mode="r", encoding=file_encoding) as f:
            content = f.read()
        if not content:
            continue
        for match in pattern.finditer(content):
            reference = match.group(1)
            if "/" in reference:
                reference = reference.split("/")[-1]
            if reference not in seen:
                seen.add(reference)
                self.filename_plaintexts.add(reference)
                if reference.endswith(".ks"):
                    self.filename_plaintexts.add(f"{reference}.scn")
    return self
