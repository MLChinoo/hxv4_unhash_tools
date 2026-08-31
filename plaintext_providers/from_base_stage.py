"""
从base.stage文件中获取背景图片文件名bgimage
"""
import logging
from pathlib import Path
from itertools import product

from jsonpath_ng.ext import parse

from plain_dict import PlainDict
from plaintext_providers import register
import utils.tjs_parser


logger = logging.getLogger(__name__)


@register(name="from_base_stage")
def collect(self: PlainDict, base_stage_filepath: str, file_encoding: str):
    try:
        base_stage_json = utils.tjs_parser.load(
            Path(base_stage_filepath),
            file_encoding
        )
        time_prefixes, season_prefixes = {""}, {""}  # 保证至少一个默认值，避免无法循环
        locale_suffixes = ["", "_jp", "_en", "_cn", "_tw"]
        time_prefix_jsonpath = parse('$.document.expression.entries[?key.value = "times"].value.entries[*].value.entries[?key.value = "prefix"].value.value')
        season_prefix_jsonpath = parse('$.document.expression.entries[?key.value = "seasons"].value.entries[*].value.entries[?key.value = "prefix"].value.value')
        image_template_jsonpath = parse('$.document.expression.entries[?key.value = "stages"].value.entries[*].value.entries[?key.value = "image"].value.value')

        time_prefixes.update(match.value for match in time_prefix_jsonpath.find(base_stage_json))
        season_prefixes.update(match.value for match in season_prefix_jsonpath.find(base_stage_json))

        for image_template_match in image_template_jsonpath.find(base_stage_json):
            image_template_filename = image_template_match.value
            for time_prefix, season_prefix, locale_suffix in product(time_prefixes, season_prefixes, locale_suffixes):
                if all((time_prefix is not None, season_prefix is not None)):
                    image_filename = (image_template_filename
                                      .replace("TIME", time_prefix)
                                      .replace("SEASON", season_prefix))
                    self.filename_plaintexts.update([
                        f"{image_filename}{locale_suffix}.png",
                        f"{image_filename}{locale_suffix}.jpg",
                        f"{image_filename}{locale_suffix}.tlg",
                        f"bgthum_{image_filename}{locale_suffix}.jpg",
                        f"bgthum_{image_filename}{locale_suffix}.png"
                    ])
    except Exception:
        logger.exception("[base.stage] 解析失败")
    return self
