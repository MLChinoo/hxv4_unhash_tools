"""
从给定的fgimage目录下查找人物.pbd文件，并获取人物立绘.tlg文件名
需要先从from_stand_files()来源获取.pbd文件
"""

import json
import subprocess
import traceback
from pathlib import Path

from plaintext_providers import register


@register(name="from_pbd_files")
def collect(self, fgimage_dir):
    def is_valid_pbd(child: Path):
        if not (child.is_file() and child.suffix == ".pbd"):
            return False
        with open(child, "rb") as f:
            return f.read(7) == b"TJS/4s0"

    for child in Path(fgimage_dir).rglob("*"):
        if is_valid_pbd(child):
            character_prefix = child.stem
            try:
                cmd_result = subprocess.run([self.config.pbd2json_exe, child.resolve()], capture_output=True, text=True, check=True)
                if cmd_result.stdout != "":
                    pbd_json = json.loads(cmd_result.stdout)
                    assert type(pbd_json) == list
                    for pbd_item in pbd_json:
                        if type(pbd_item) == dict and "layer_id" in pbd_item.keys():
                            self.filename_plaintexts.add(
                                f'{character_prefix}_{pbd_item["layer_id"]}.tlg'
                            )
                else:
                    raise RuntimeError(f"fail to convert pbd to json: {child}")
            except Exception:
                traceback.print_exc()
    return self
