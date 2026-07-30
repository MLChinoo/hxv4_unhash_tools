"""
从replay.ks获取影片文件名video
实际上macro.ks也存在影片（如nene_change和tsumu_change），但数量极少故暂不处理
同时保留命名为add_movies而不是from_replay_ks
"""

import re
from itertools import product

from plaintext_providers import register


@register(name="from_replay_ks")
def collect(self, replay_ks_filepath, file_encoding: str = "utf-16le"):
    movie_names = ["op"]
    languages = ("en", "cn", "tw")  # 日语无前缀
    extensions = ("mp4", "wmv")
    pattern = r'\[(?:sysmovie|edmovie)\s+file=([^\s\]]+)\s*\]'
    with open(replay_ks_filepath, mode="r", encoding=file_encoding) as f:
        replay_ks = f.read()
    if replay_ks == "":
        print("[replay.ks] 无法读取")
        return self
    replay_ks = replay_ks.replace("\ufeff", "")
    movie_names.extend(re.findall(pattern, replay_ks))
    for movie_name, language, extension in product(movie_names, languages, extensions):
        self.filename_plaintexts.update([
            f"{movie_name}.{extension}",
            f"{language}_{movie_name}.{extension}",
            f"{movie_name}1080.{extension}",
            f"{language}_{movie_name}1080.{extension}",
            f"{movie_name}_1080.{extension}",
            f"{language}_{movie_name}_1080.{extension}",
            f"{movie_name}720p.{extension}",
            f"{language}_{movie_name}720p.{extension}",
        ])
    print(f"[replay.ks] 提取了 {len(movie_names)} 个影片名称")
    return self
