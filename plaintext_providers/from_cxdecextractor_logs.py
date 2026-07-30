"""
从CxdecExtractor生成的FileNameHash.log和DirectoryHash.log中获取文件名和路径名
"""

import traceback
from pathlib import Path

from plaintext_providers import register


@register(name="from_cxdecextractor_logs")
def collect(self, directory_hash_log_filepath: str, filename_hash_log_filepath: str, file_encoding: str = "utf-16le"):
    directory_hash_log_filepath = Path(directory_hash_log_filepath)
    filename_hash_log_filepath = Path(filename_hash_log_filepath)
    filename_count = 0
    pathname_count = 0

    if filename_hash_log_filepath.exists():
        try:
            with open(filename_hash_log_filepath, mode="r", encoding=file_encoding) as f:
                for line in f:
                    line = line.strip().replace("\ufeff", "")
                    if "##YSig##" not in line:
                        continue
                    filename = line.split("##YSig##", 1)[0].strip()
                    if filename and filename != "%EmptyString%":
                        self.filename_plaintexts.add(filename)
                        filename_count += 1
        except Exception:
            traceback.print_exc()

    if directory_hash_log_filepath.exists():
        try:
            with open(directory_hash_log_filepath, mode="r", encoding=file_encoding) as f:
                for line in f:
                    line = line.strip().replace("\ufeff", "")
                    if "##YSig##" not in line:
                        continue
                    pathname = line.split("##YSig##", 1)[0].strip()
                    if pathname and pathname != "%EmptyString%":
                        self.pathname_plaintexts.add(pathname)
                        pathname_count += 1
        except Exception:
            traceback.print_exc()

    if filename_count > 0 or pathname_count > 0:
        print(
            f"[cxdecextractor_logs] 提取了 {filename_count} 个文件名、"
            f"{pathname_count} 个路径名"
        )
    return self
