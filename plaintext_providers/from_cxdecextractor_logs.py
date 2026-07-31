"""
从CxdecExtractor生成的FileNameHash.log和DirectoryHash.log中获取文件名和路径名
"""

import traceback
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_cxdecextractor_logs")
def collect(self: PlainDict, directory_hash_log_filepath: str, filename_hash_log_filepath: str):
    directory_hash_log_filepath = Path(directory_hash_log_filepath)
    filename_hash_log_filepath = Path(filename_hash_log_filepath)
    if filename_hash_log_filepath.exists():
        try:
            with open(filename_hash_log_filepath, mode="r", encoding="utf-16le") as f:
                for line in f:
                    line = line.strip().replace("\ufeff", "")
                    if "##YSig##" not in line:
                        continue
                    filename = line.split("##YSig##", 1)[0].strip()
                    if filename and filename != "%EmptyString%":
                        self.filename_plaintexts.add(filename)
        except Exception:
            traceback.print_exc()

    if directory_hash_log_filepath.exists():
        try:
            with open(directory_hash_log_filepath, mode="r", encoding="utf-16le") as f:
                for line in f:
                    line = line.strip().replace("\ufeff", "")
                    if "##YSig##" not in line:
                        continue
                    pathname = line.split("##YSig##", 1)[0].strip()
                    if pathname and pathname != "%EmptyString%":
                        self.pathname_plaintexts.add(pathname)
        except Exception:
            traceback.print_exc()
    return self
