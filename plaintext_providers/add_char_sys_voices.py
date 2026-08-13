"""
添加各人物的系统语音，从charvoice.csv获取人物前缀名，从sysse.ini获取系统语音文件名模板
"""

import csv
from itertools import product

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="add_char_sys_voices")
def collect(self: PlainDict, charvoice_csv_filepath: str, sysse_ini_filepath: str, file_encoding: str = "utf-16le"):
    def get_character_prefix(charvoice_csv_filepath: str) -> set[str]:
        prefixes = set()
        with open(charvoice_csv_filepath, mode="r", encoding=file_encoding) as f:
            charvoice_csv = csv.reader(f)
            for row in charvoice_csv:
                if len(row) == 0:
                    continue
                header = row[0].replace("\ufeff", "")  # remove bom
                if not header.startswith("#") and not header.startswith("DEFAULT") and len(row) > 1:
                    char_prefix: str = row[1].replace("%s", "").split("_")[0]
                    prefixes.add(char_prefix)
        return prefixes
    def get_sys_voice_filename_template(sysse_ini_filepath: str) -> set[str]:
        templates = set()
        with open(sysse_ini_filepath, mode="r", encoding=file_encoding) as f:
            content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#") or line.startswith("?"):
                continue
            if "=" not in line:
                continue
            left_side = line.split("=", 1)[0].strip()
            right_side = line.split("=", 1)[1].strip()
            if right_side.startswith("@") or right_side.startswith("alias"):
                continue
                
            sound_name: str = right_side.split(":")[0].strip()
            if "%s" in sound_name:
                assert "sysvo.format" in left_side
                templates.add(sound_name)
            elif sound_name and " " not in sound_name:
                for extension in ["ogg", "ogg.sli", "opus", "opus.sli", "ini"]:
                    self.filename_plaintexts.add(f"{sound_name}.{extension}")
        return templates
    
    for prefix, template in product(
            get_character_prefix(charvoice_csv_filepath),
            get_sys_voice_filename_template(sysse_ini_filepath)):
        self.filename_plaintexts.add(f"{template.replace('%s', prefix)}.ogg")
    return self
