"""
从背景对话文件 (e.g. bgv102_02_恵凪会話.csv) 中获取语音文件名
此文件名分布在各个scn中，因此需先跑一遍scan_psb_and_decompile()
此文件一般位于voice包中，因此需指定跑过一遍脚本后的voice文件夹
"""

import csv
from pathlib import Path

from plaintext_providers import register


@register(name="from_bgv_csv")
def collect(self, voice_dir, file_encoding: str = "utf-16le"):
    count = 0
    for child in Path(voice_dir).rglob("*"):
        # 假设文件名以bgv开头，扩展名为.csv
        if all([child.is_file(), child.stem.startswith("bgv"), child.suffix == ".csv"]):
            with open(child, mode="r", encoding=file_encoding) as f:
                bgv_csv = csv.reader(f)
                for row in bgv_csv:
                    if len(row) > 2 and not row[0].replace("\ufeff", "").startswith("#"):
                        voice_name = row[2]
                        self.filename_plaintexts.update([
                            f"{voice_name}.ogg",
                            f"{voice_name}.ogg.sli",
                            f"{voice_name}.opus",
                            f"{voice_name}.opus.sli",
                            f"{voice_name}.ini"
                        ])
                        count += 1
    if count > 0:
        print(f"[bgv_csv] 提取了 {count} 个背景语音条目")
    return self
