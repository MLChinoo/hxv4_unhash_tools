"""
从base.stage文件中获取背景图片文件名bgimage
"""
import traceback
from pathlib import Path
from itertools import product

from plain_dict import PlainDict
from plaintext_providers import register
import utils.tjs_parser


@register(name="from_base_stage")
def collect(self: PlainDict, base_stage_filepath: str, file_encoding: str):
    try:
        base_stage_json = utils.tjs_parser.load(
            Path(base_stage_filepath),
            file_encoding
        )
        time_prefixes, season_prefixes = {""}, {""}  # 保证至少一个默认值，避免无法循环

        for entry_1 in base_stage_json["document"]["expression"]["entries"]:
            if entry_1["key"]["value"] == "times":
                for entry_2 in entry_1["value"]["entries"]:
                    for entry_3 in entry_2["value"]["entries"]:
                        if entry_3["key"]["value"] == "prefix":
                            time_prefixes.add(entry_3["value"]["value"])
            elif entry_1["key"]["value"] == "seasons":
                for entry_2 in entry_1["value"]["entries"]:
                    for entry_3 in entry_2["value"]["entries"]:
                        if entry_3["key"]["value"] == "prefix":
                            season_prefixes.add(entry_3["value"]["value"])

        count = 0
        for entry_1 in base_stage_json["document"]["expression"]["entries"]:
            if entry_1["key"]["value"] == "stages":
                for entry_2 in entry_1["value"]["entries"]:
                    for entry_3 in entry_2["value"]["entries"]:
                        if entry_3["key"]["value"] == "image":
                            image_template_filename = entry_3["value"]["value"]
                            for time_prefix, season_prefix in product(time_prefixes, season_prefixes):
                                if all((time_prefix is not None, season_prefix is not None)):
                                    image_filename = (image_template_filename
                                                      .replace("TIME", time_prefix)
                                                      .replace("SEASON", season_prefix))
                                    self.filename_plaintexts.update([
                                        f"{image_filename}.png",
                                        f"{image_filename}.jpg",
                                        f"{image_filename}.tlg",
                                        f"bgthum_{image_filename}.jpg",
                                        f"bgthum_{image_filename}.png"
                                    ])
                                    count += 1
        print(f"[base.stage] 提取了 {count} 个背景图条目")
    except Exception:
        print("[base.stage] 解析失败:")
        traceback.print_exc()
    return self
