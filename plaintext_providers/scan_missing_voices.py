"""
寻找可能遗漏的语音文件
某些语音存在于voice目录中，但未被任何scn引用，根本不可能在正常游戏流程中出现（即“废案语音”，例如宁宁有30个左右），
这时即可利用语音文件名编号连续的特点，来尽可能寻找这些语音。
"""

import csv
import re
from pathlib import Path
from collections.abc import Iterable

from plaintext_providers import register


@register(name="find_missing_voices")
def collect(self, voice_dirs: Iterable, check_file_existence = False):
    prefixes_map = {}  # anj_000: [4, 90] / anj_loop: [2, 64]

    def handle_voice_name(voice_name: str):  # anj_000_0090 / anj_loop_64
        if "_" not in voice_name:
            # print(f"illegal missing voice name: {voice_name}")
            return
        prefix, num = voice_name.rsplit("_", 1)  # anj_000, 0090 / anj_loop, 64
        if result := re.match(r'^\d+', num):
            first_match: str = result.group(0)
            num, size = int(first_match), len(first_match)  # 90, 4 / 64, 2
            if prefix not in prefixes_map:
                prefixes_map[prefix] = [size, num]
            else:
                ori_size = prefixes_map[prefix][0]
                if size != ori_size:
                    print(f"{voice_name} suffix size changed: {ori_size} -> {size}")
                if num > prefixes_map[prefix][1]:
                    prefixes_map[prefix][1] = num

    for voice_dir in voice_dirs:
        for child in Path(voice_dir).iterdir():
            if child.is_file():  # anj_000_0090.ogg / anj_loop_64.ogg / bgv102_02_恵凪会話.csv
                match child.suffix:
                    case ".ogg" | ".sli":
                        handle_voice_name(child.stem)
                    case ".csv":
                        if child.stem.startswith("bgv"):
                            with open(child, mode="r", encoding="utf-16le") as f:
                                bgv_csv = csv.reader(f)
                                for row in bgv_csv:
                                    if len(row) > 0 and not row[0].replace("\ufeff", "").startswith("#"):
                                        handle_voice_name(row[2])

    for prefix, _ in prefixes_map.items():
        size, maxnum = _
        maxnum += 5
        for num in range(1, maxnum + 1):
            voice_name = f"{prefix}_{num:0{size}d}"
            for suffix in {"", "a", "b", "c", "_ref", "_ref2"}:  # 暂时未发现其它字母后缀
                voice_name_suffix = voice_name + suffix
                self.filename_plaintexts.update([
                    f"{voice_name_suffix}.ogg",
                    f"{voice_name_suffix}.ogg.sli"
                ])
                if check_file_existence:
                    if not any(((Path(vd) / f"{voice_name_suffix}.ogg").exists() for vd in voice_dirs)):
                        print(f"found possible missing voice: {voice_name_suffix}")

    return self
