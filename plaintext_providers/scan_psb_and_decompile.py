"""
扫描给定目录下的文件，对可能的psb文件进行decompile并获取信息
"""

import json
import pickle
import os
import shutil
import subprocess
import traceback
from pathlib import Path
from contextlib import suppress

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="scan_psb_and_decompile")
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

    def handle_data_item(data_item: dict):
        if data_item.get("name") in ("bgm", "live", "liveout") and "replay" in data_item.keys():
            # 获取背景音乐文件名  bgm
            filename = data_item["replay"]["filename"]
            if filename is not None:
                self.filename_plaintexts.update([
                    f"{filename}.ogg",
                    f"{filename}.ogg.sli",
                    f"{filename}.opus",
                    f"{filename}.opus.sli",
                    f"{filename}.mchx",
                    f"{filename}.mchx.sli"
                ])
        elif data_item.get("name") in ("lse", "lse2", "se", "se2") and "replay" in data_item.keys():
            # sound
            filename_raw: str = data_item["replay"]["filename"]
            if filename_raw is not None:
                filenames = filename_raw.split("|")
                for filename in filenames:
                    self.filename_plaintexts.update([
                        f"{filename}.ogg",
                        f"{filename}.ogg.sli",
                        f"{filename}.ini"
                    ])
        elif data_item.get("name") == "stage" and "redraw" in data_item.keys():
            # 获取背景图片文件名  bgimage
            filename = data_item["redraw"]["imageFile"]["file"]
            self.filename_plaintexts.update([
                f"{filename}.png",
                f"bgthum_{filename}.jpg"
            ])
        elif data_item.get("class") in ("msgwin", "character"):
            # 获取人物stand文件名  fgimage
            standname_with_ext = None
            if "redraw" in data_item.keys():
                standname_with_ext = data_item["redraw"]["imageFile"]["file"]
                if "clip" in data_item["redraw"].keys():
                    imagename = data_item["redraw"]["clip"]["image"]
                    self.filename_plaintexts.add(
                        f"{imagename}.png"
                    )
            elif "stand" in data_item.keys():
                standname_with_ext = data_item["stand"]["file"]
            if type(standname_with_ext) == str:
                if standname_with_ext.endswith(".stand"):
                    self.filename_plaintexts.add(
                        f"{standname_with_ext}"
                    )
                else:
                    print(f"bad stand name, ignored: {standname_with_ext}")
        elif data_item.get("class") == "event":
            if data_item.get("name") == "ev" and "redraw" in data_item.keys():
                # 在lines中获取image
                filename_rawline: str = data_item["redraw"]["imageFile"]["file"]  # "mtile,ed_nicola_roll.tjs"
                for filename in filename_rawline.split(","):
                    filename = filename.strip()
                    if "." in filename:  # ed_nicola_roll.tjs
                        self.filename_plaintexts.add(filename)
                        if filename.endswith(".tjs"): # ed_nicola_roll.tjs
                            for locale in ("_jp", "_en", "_cn", "_tw"):
                                self.filename_plaintexts.add(filename.replace(".tjs", f"{locale}.ini"))
                    else:  # 空_夜
                        self.filename_plaintexts.add(f"{filename}.png")
            elif data_item.get("name") == "bg_voice" and "redraw" in data_item.keys():
                # 背景对话文件 bg_voice (e.g. bgv007_07_歓声.csv)
                filename_with_ext = data_item["redraw"]["imageFile"]["file"]["storage"]
                self.filename_plaintexts.add(
                    f"{filename_with_ext}"
                )
        elif data_item.get("class") == "phonechat" and data_item.get("name") == "phonescreen" and "redraw" in data_item.keys():
            # 获取气泡聊天背景图片
            filename = data_item["redraw"]["imageFile"]["file"]
            self.filename_plaintexts.add(
                f"{filename}.tlg"
            )
        elif data_item.get("class") == "sdlayer" and "redraw" in data_item.keys():
            # sd图层
            filename = data_item["redraw"]["imageFile"]["file"]
            self.filename_plaintexts.add(
                f"{filename}.png"
            )
        elif data_item.get("class") in ("event2", "stage2") and "redraw" in data_item.keys():
            # image
            filename = None
            if "clip" in data_item["redraw"].keys():
                filename = data_item["redraw"]["clip"]["image"]
            elif "imageFile" in data_item["redraw"].keys():
                filename = data_item["redraw"]["imageFile"]["file"]
            if filename is not None:
                self.filename_plaintexts.add(
                    f"{filename}.png"
                )

    def handle_data_block(data_block: list):
        # lines和texts里某些data字段结构是一致的，因此可以封装成一个共同方法进行处理
        for data in data_block:
            if type(data) == list:
                for data_item in data:
                    if type(data_item) == dict:
                        handle_data_item(data_item)

    def handle_voice(voice_filenames_raw: str):  # fanB_412_0012.ogg|DL_回想
        base_voice_extensions = {"ogg", "ogg.sli", "opus", "opus.sli", "ini"}
        voice_filenames = voice_filenames_raw.split("|")
        for voice_filename in voice_filenames:
            if "." in voice_filename:
                if voice_filename.count(".") > 1:
                    print(f"warning: multiple extensions file - {voice_filename}")
                voice_name, extension = voice_filename.split(".", 1)
            else:
                voice_name, extension = voice_filename, None
            voice_extensions = base_voice_extensions.copy()
            if extension is not None:
                voice_extensions.add(extension)
            for voice_extension in voice_extensions:
                self.filename_plaintexts.update([
                    f"{voice_name}.{voice_extension}"
                ])

    if not os.path.exists(self.config.psb_type_cache_pkl):
        open(self.config.psb_type_cache_pkl, mode="wb")
    with suppress(pickle.UnpicklingError, EOFError):
        with open(self.config.psb_type_cache_pkl, mode="rb") as ptcf:
            psb_type_cache = pickle.load(ptcf)

    for root, dirs, files in os.walk(scn_dir):
        for file in files:
            filepath = os.path.join(root, file)
            file_prefix = str(Path(filepath).parent.relative_to(self.config.rename_dir)).replace("\\", "_") + "_"
            if is_psb_file(filepath)\
                    and file_prefix + file not in psb_type_cache["pimg"]\
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
                        # scn psb
                        psb_type_cache["scn"].add(file_prefix + file)

                        # 从name字段获取scn原文件名
                        self.filename_plaintexts.add(f"{psb_json['name']}.scn")

                        for scene in psb_json["scenes"]:
                            if "texts" in scene.keys():
                                for text in scene["texts"]:
                                    for text_item in text:
                                        if type(text_item) == list:
                                            for text_item_item in text_item:
                                                if type(text_item_item) == dict and "voice" in text_item_item.keys():
                                                    # 获取语音文件名  voice
                                                    voice_source = text_item_item
                                                    handle_voice(voice_source["voice"])

                                        elif type(text_item) == dict:
                                            if "data" in text_item.keys():
                                                handle_data_block(text_item["data"])
                                            if "phonechat" in text_item.keys():
                                                for chat in text_item["phonechat"]:
                                                    assert type(chat) == dict
                                                    icon = chat["icon"]
                                                    self.filename_plaintexts.add(
                                                        f"chaticon_{icon}.png"
                                                    )
                                                    stamp = chat.get("stamp")
                                                    self.filename_plaintexts.add(
                                                        f"{stamp}.png"
                                                    )
                                            if "loopVoiceList" in text_item.keys():
                                                for loop_voice in text_item["loopVoiceList"]:
                                                    handle_voice(loop_voice["voice"])

                            for line in scene["lines"]:  # 0000
                                if type(line) == list:
                                    for index, line_item in enumerate(line):
                                        if type(line_item) == dict and "data" in line_item.keys():
                                            handle_data_block(line_item["data"])

                                        elif type(line_item) == list:
                                            for item in line_item:
                                                if type(item) == dict:
                                                    handle_data_item(item)

                                        elif type(line_item) == str:
                                            if line[index-1] == "voice":
                                                # 某些语音藏在lines的playvoice行中... (e.g. anj_102_0016)
                                                handle_voice(line_item)


                    elif "height" in psb_json and "width" in psb_json:  # and "layers" in psb_json
                        # pimg psb
                        psb_type_cache["pimg"].add(file_prefix + file)
                        json_f.close()
                        os.remove(json_filepath)

                    elif psb_json.get("id") == "motion":
                        # motion psb
                        psb_type_cache["motion"].add(file_prefix + file)
                        json_f.close()
                        os.remove(json_filepath)

                    else:
                        json_f.close()
                        os.remove(json_filepath)
                        raise NotImplementedError(f"{file}\n{psb_json.keys()}")
                    json_f.close()
                except Exception:
                    traceback.print_exc()
    with open(self.config.psb_type_cache_pkl, mode="wb") as ptcf:
        pickle.dump(psb_type_cache, ptcf)
    for root, dirs, files in os.walk(self.config.temp_dir):
        for d in dirs:
            shutil.rmtree(os.path.join(self.config.temp_dir, d))
    return self
