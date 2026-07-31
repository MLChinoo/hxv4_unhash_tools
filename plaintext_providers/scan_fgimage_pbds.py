"""
从给定的fgimage目录下查找人物.pbd文件，并获取人物立绘.tlg文件名
需要先从scan_fgimage_stands()来源获取.pbd文件
"""

import json
import subprocess
import traceback
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="scan_fgimage_pbds")
def collect(self: PlainDict, fgimage_dir: str):
    def is_valid_pbd(child: Path):
        if not (child.is_file() and child.suffix == ".pbd"):
            return False
        with open(child, "rb") as f:
            return f.read(7) == b"TJS/4s0"

    for child in Path(fgimage_dir).rglob("*"):
        if is_valid_pbd(child):
            # _0本身就是character_prefix的一部分，没有必要额外处理（梓a.pbd, 梓a_0.pbd）
            character_prefix = child.stem
            try:
                cmd_result = subprocess.run([self.config.pbd2json_exe, child.resolve()], capture_output=True, text=True, check=True)
                if cmd_result.stdout != "":
                    pbd_json = json.loads(cmd_result.stdout)
                    assert type(pbd_json) == list
                    for pbd_item in pbd_json:
                        if type(pbd_item) == dict and "layer_id" in pbd_item.keys():
                            self.filename_plaintexts.update([
                                f'{character_prefix}_{pbd_item["layer_id"]}.tlg',
                                f'{character_prefix}_{pbd_item["layer_id"]}.png'
                            ])
                else:
                    raise RuntimeError(f"fail to convert pbd to json: {child}")
            except Exception:
                traceback.print_exc()
    return self
