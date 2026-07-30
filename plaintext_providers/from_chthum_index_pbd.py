"""
从_chthum_index.pbd文件中获取人物立绘缩略图
"""

import json
import subprocess
import traceback
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_chthum_index_pbd")
def collect(self: PlainDict, chthum_index_pbd_filepath):
    def is_valid_pbd(child: Path):
        if not (child.is_file() and child.suffix == ".pbd"):
            return False
        with open(child, "rb") as f:
            return f.read(7) == b"TJS/ns0"

    child = Path(chthum_index_pbd_filepath)
    if is_valid_pbd(child):
        try:
            cmd_result = subprocess.run([self.config.pbd2json_exe, child.resolve()], capture_output=True, text=True, check=True)
            if cmd_result.stdout != "":
                pbd_json = json.loads(cmd_result.stdout)
                assert type(pbd_json) == dict
                for filename in pbd_json.values():
                    if "." not in filename:
                        self.filename_plaintexts.update([
                            f"{filename}.png",
                            f"{filename}.jpg"
                        ])
                    else:
                        self.filename_plaintexts.add(filename)
            else:
                raise RuntimeError(f"fail to convert pbd to json: {child}")
        except Exception:
            traceback.print_exc()
    return self
