"""
从TLGref文件中获取被引用的TLG文件名
"""

import struct
from pathlib import Path

from plaintext_providers import register


@register(name="scan_evimage_tlgrefs")
def collect(self, evimage_dir: str):
    count = 0
    for child in Path(evimage_dir).rglob("*"):
        if not child.is_file():
            continue

        try:
            with open(child, "rb") as f:
                header = f.read(0x80)
            if len(header) < 0x30 or header[:6] != b"TLGref":
                continue

            raw_filename = header[0x2c:]
            characters = []
            for index in range(0, len(raw_filename) - 1, 2):
                character_code = struct.unpack_from(
                    "<H",
                    raw_filename,
                    index
                )[0]
                if character_code == 0:
                    break
                if 0x20 <= character_code < 0x10000:
                    characters.append(chr(character_code))
                else:
                    characters = []
                    break

            filename = "".join(characters)
            if filename and ".tlg" in filename:
                self.filename_plaintexts.add(filename)
                count += 1
        except OSError:
            pass

    if count > 0:
        print(f"[tlgref] 提取了 {count} 个被引用的 TLG 文件名")
    return self
