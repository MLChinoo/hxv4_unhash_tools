"""
从replay.ks获取影片文件名video
实际上macro.ks也存在影片（如nene_change和tsumu_change），但数量极少故暂不处理
同时保留命名为add_movies而不是from_replay_ks
"""

import re
from itertools import product

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_replay_ks")
def collect(self: PlainDict, replay_ks_filepath, file_encoding: str = "utf-16le"):
    movie_names = ["op"]
    locales = ("", "jp_", "en_", "cn_", "tw_")
    extensions = ("mp4", "wmv")
    pattern = r'\[(?:sysmovie|edmovie)\s+file=([^\s\]]+)\s*\]'
    with open(replay_ks_filepath, mode="r", encoding=file_encoding) as f:
        replay_ks = f.read()
    if replay_ks == "":
        print("[replay.ks] 无法读取")
        return self
    replay_ks = replay_ks.replace("\ufeff", "")
    movie_names.extend(re.findall(pattern, replay_ks))
    for movie_name, locale, extension in product(movie_names, locales, extensions):
        self.filename_plaintexts.update([
            f"{locale}{movie_name}.{extension}",
            f"{locale}{movie_name}1080.{extension}",
            f"{locale}{movie_name}_1080.{extension}",
            f"{locale}{movie_name}720p.{extension}",
        ])
    return self
