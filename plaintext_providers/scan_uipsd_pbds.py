"""
从给定的uipsd目录下查找.pbd文件，并获取.tlg文件名
建议和scan_uipsd_multi_lang()一起多次循环使用来提升覆盖率。
"""
import json
import subprocess
import traceback
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="scan_uipsd_pbds")
def collect(self: PlainDict, uipsd_dir: str):
    def is_valid_pbd(child: Path):
        if not (child.is_file()):
            return False
        with open(child, "rb") as f:
            return f.read(7) == b"TJS/ns0"

    for child in Path(uipsd_dir).rglob("*"):
        print(child.resolve())
        if is_valid_pbd(child):
            try:
                cmd_result = subprocess.run([self.config.pbd2json_exe, child.resolve()], capture_output=True, text=True, check=True)
                if cmd_result.stdout != "":
                    pbd_json = json.loads(cmd_result.stdout)
                    if pbd_json["holdimage"] is not None:
                        for hi in pbd_json["holdimage"]:
                            self.filename_plaintexts.add(f"{hi}.tlg")
                    # result -> uistates -> storage 里也有文件名，均应包含在holdimage中，暂不解析
                else:
                    raise RuntimeError(f"fail to convert pbd to json: {child}")
            except Exception:
                traceback.print_exc()
    return self
