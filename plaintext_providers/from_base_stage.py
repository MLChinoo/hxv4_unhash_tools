"""
从base.stage文件中获取背景图片文件名bgimage
"""

import json5
from itertools import product
from utils.tjs_parser import parse_base_stage_to_json5

from plaintext_providers import register


@register(name="from_base_stage")
def collect(self, base_stage_filepath: str):
    with open(base_stage_filepath, mode="r", encoding="utf-16le") as f:
        base_stage: dict = json5.loads(parse_base_stage_to_json5(f.read()))
    time_prefixes, season_prefixes = {""}, {""}  # 保证至少一个默认值，避免无法循环
    for key, value in base_stage.items():
        if type(value) == dict:
            if key == "times":
                for time in value.values():
                    time_prefixes.add(time.get("prefix"))
            elif key == "seasons":
                for season in value.values():
                    season_prefixes.add(season.get("prefix"))
            elif key != "stages":
                pass  # unknown classification...?
    for stage in base_stage["stages"].values():
        image_filename_template: str = stage["image"]
        for time_prefix, season_prefix in product(time_prefixes, season_prefixes):
            if all((time_prefix is not None, season_prefix is not None)):
                image_filename = (image_filename_template
                                  .replace("TIME", time_prefix)
                                  .replace("SEASON", season_prefix))
                self.filename_plaintexts.update([
                    f"{image_filename}.png",
                    f"bgthum_{image_filename}.jpg"
                ])
    return self
