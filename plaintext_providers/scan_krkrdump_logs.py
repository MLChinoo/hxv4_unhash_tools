"""
从KrkrDump的log中获取文件名
适用于从未在之前发行的游戏中出现的、以及无规律可获取其文件名的文件，动态运行一下也许有意外收获...?
"""

import logging
import os
import re

from plain_dict import PlainDict
from plaintext_providers import register


logger = logging.getLogger(__name__)


@register(name="from_krkrdump_logs")
def collect(self: PlainDict, krkrdump_dir):
    for filename in os.listdir(krkrdump_dir):
        if all((filename.startswith("KrkrDump-"), filename.endswith(".log"))):
            logger.info(f"current log: {filename}")
            filepath = os.path.join(krkrdump_dir, filename)
            with open(filepath, mode="r", encoding="UTF-8") as log_f:
                krkrdump_log = log_f.readlines()
            for line in krkrdump_log:
                    match = re.search(r'"([^"]*)"', line)
                    if match:
                        content = match.group(1)
                        if "NameHash: " in line:
                            self.filename_plaintexts.add(content)
                        elif "PathHash: " in line:
                            self.pathname_plaintexts.add(content)
    return self
