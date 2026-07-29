"""
添加各人物的系统语音，从charvoice.csv获取人物前缀名，语音后缀名来自天使嚣嚣trial，可能涵盖不全
"""

import csv

from plaintext_providers import register


@register(name="add_char_sys_voices")
def collect(self, charvoice_csv_filepath):
    sys_voice_suffixes = (
        "after",
        "attention0",
        "attention1",
        "attention2",
        "attention3",
        "backlog",
        "chart",
        "config",
        "config_easy",
        "custom",
        "dialog",
        "end",
        "extra",
        "extra_bu",
        "extra_cg",
        "extra_scene",
        "game",
        "game2",
        "goodbye",
        "jump",
        "load",
        "mouse",
        "pad",
        "rec",
        "reset",
        "save",
        "shortcut",
        "sound",
        "text",
        "tittle",
        "tittleback",
        "voice",
        "volume",
        "window",
        "yuzu",

        "title",
        "titleback"
    )
    with open(charvoice_csv_filepath, mode="r", encoding="utf-16le") as f:
        charvoice_csv = csv.reader(f)
        for row in charvoice_csv:
            if len(row) > 0:
                header = row[0].replace("\ufeff", "")  # remove bom
                if not header.startswith("#") and not header.startswith("DEFAULT"):
                    char_prefix = row[1].split("_")[0]
                    for sys_voice_suffix in sys_voice_suffixes:
                        self.filename_plaintexts.add(f"{char_prefix}_{sys_voice_suffix}.ogg")
    return self
