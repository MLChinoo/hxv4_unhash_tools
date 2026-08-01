"""
扫描给定目录下的文件，对可能的psb文件进行decompile并获取所有文件引用
"""

import json
import logging
import os
import pickle
import re
import shutil
import subprocess
from contextlib import suppress
from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register


logger = logging.getLogger(__name__)


@register(name="scan_psb_and_decompile_re")
def collect(self: PlainDict, scn_dir: str):
    def is_psb_file(path) -> bool:
        path = Path(path)
        if not path.is_file():
            return False
        try:
            with path.open("rb") as f:
                header = f.read(3)
                return header == b"PSB" or header == b"mdf"
        except OSError:
            return False

    def convert_to_custom_extension(filename: str, new_extension: str) -> str:
        if not new_extension.startswith("."):
            new_extension = "." + new_extension
        if "." in filename and not filename.startswith("."):
            base = ".".join(filename.split(".")[:-1])
        else:
            base = filename
        return base + new_extension

    psb_type_cache = {
        "scn": set(),
        "pimg": set(),
        "motion": set()
    }
    image_names = set()
    sound_names = set()
    scenario_names = set()

    if not os.path.exists(self.config.psb_type_cache_pkl):
        open(self.config.psb_type_cache_pkl, mode="wb")
    with suppress(pickle.UnpicklingError, EOFError):
        with open(self.config.psb_type_cache_pkl, mode="rb") as ptcf:
            psb_type_cache = pickle.load(ptcf)

    for root, dirs, files in os.walk(scn_dir):
        for file in files:
            filepath = os.path.join(root, file)
            file_prefix = str(Path(filepath).parent.relative_to(self.config.rename_dir)).replace("\\", "_")+ "_"
            if is_psb_file(filepath) \
                    and file_prefix + file not in psb_type_cache["pimg"] \
                    and file_prefix + file not in psb_type_cache["motion"]:
                try:
                    json_filename = file_prefix + convert_to_custom_extension(file, ".json")
                    json_filepath = os.path.join(self.config.temp_dir, json_filename)

                    if not os.path.exists(json_filepath):
                        shutil.copy(filepath, temp_filepath := os.path.join(self.config.temp_dir, file_prefix + file))
                        subprocess.run([self.config.psbdecompile_exe, '-raw', temp_filepath], check=True)
                        os.remove(temp_filepath)
                        resx_json_filename = file_prefix + convert_to_custom_extension(file, ".resx.json")
                        resx_json_filepath = os.path.join(self.config.temp_dir, resx_json_filename)
                        os.remove(resx_json_filepath)

                    json_f = open(json_filepath, mode="r", encoding="UTF-8")
                    psb_json: dict = json.load(json_f)
                    if "scenes" in psb_json and "name" in psb_json:
                        psb_type_cache["scn"].add(file_prefix + file)

                        json_f.seek(0)
                        content = json_f.read()
                        for match in re.finditer(r'"file":\s*"([^"]+)"', content):
                            image_names.add(match.group(1))
                        for match in re.finditer(r'"image":\s*"([^"]+)"', content):
                            image_names.add(match.group(1))
                        for match in re.finditer(r'"filename":\s*"([^"]+)"', content):
                            sound_names.add(match.group(1))
                        for match in re.finditer(r'"storage":\s*"([^"]+)"', content):
                            scenario_names.add(match.group(1))

                    elif "height" in psb_json and "width" in psb_json:
                        psb_type_cache["pimg"].add(file_prefix + file)
                        json_f.close()
                        os.remove(json_filepath)

                    elif psb_json.get("id") == "motion":
                        psb_type_cache["motion"].add(file_prefix + file)
                        json_f.close()
                        os.remove(json_filepath)

                    else:
                        json_f.close()
                        os.remove(json_filepath)
                        raise NotImplementedError(
                            f"{file}\n{psb_json.keys()}"
                        )
                    json_f.close()
                except Exception:
                    logger.exception("处理 PSB 文件失败")

    for image_name in image_names:
        if image_name.startswith("ev") or image_name.startswith("sd") or image_name.endswith(".stand"):
            continue
        for extension in (".jpg", ".png", ".tlg", ".pimg", ".sinfo"):
            self.filename_plaintexts.add(
                f"{image_name}{extension}"
            )
        self.filename_plaintexts.update([
            f"bgthum_{image_name}.jpg",
            f"bgthum_{image_name}.png"
        ])
    for sound_name in sound_names:
        for extension in (".ogg", ".ogg.sli", ".opus", ".opus.sli", ".mchx", ".mchx.sli", ".ini"):
            self.filename_plaintexts.add(
                f"{sound_name}{extension}"
            )
    for scenario_name in scenario_names:
        if not scenario_name.endswith(".ks"):
            continue
        self.filename_plaintexts.update([
            scenario_name,
            f"{scenario_name}.scn"
        ])

    with open(self.config.psb_type_cache_pkl, mode="wb") as ptcf:
        pickle.dump(psb_type_cache, ptcf)
    for root, dirs, files in os.walk(self.config.temp_dir):
        for directory in dirs:
            shutil.rmtree(os.path.join(self.config.temp_dir, directory))
    return self
