# 此文件由 utils/generate_provider_typing.py 自动生成，请勿手动修改。
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from plain_dict import PlainDict


class PlainDictProviders:
    def add_char_sys_voices(self, charvoice_csv_filepath) -> PlainDict:
        ...

    def add_movies(self, replay_ks_filepath) -> PlainDict:
        ...

    def duplicate_lower(self) -> PlainDict:
        ...

    def find_missing_voices(self, voice_dirs: Iterable, check_file_existence = False) -> PlainDict:
        ...

    def from_base_stage(self, base_stage_filepath: str) -> PlainDict:
        ...

    def from_bgv_csv(self, voice_dir) -> PlainDict:
        ...

    def from_cglist_csv(self, cglist_csv_filepath: str) -> PlainDict:
        ...

    def from_chthum_index_pbd(self, chthum_index_pbd_filepath) -> PlainDict:
        ...

    def from_imagediffmap_csv(self, imagediffmap_csv_filepath) -> PlainDict:
        ...

    def from_krkrdump_logs(self, krkrdump_dir) -> PlainDict:
        ...

    def from_pbd_files(self, fgimage_dir) -> PlainDict:
        ...

    def from_savelist_csv(self, savelist_csv_filepath) -> PlainDict:
        ...

    def from_scenelist_csv(self, scenelist_csv_filepath) -> PlainDict:
        ...

    def from_soundlist_csv(self, soundlist_csv_filepath) -> PlainDict:
        ...

    def from_stand_files(self, fgimage_dir) -> PlainDict:
        ...

    def from_unobfuscated_directory(self, base_dir: str) -> PlainDict:
        ...

    def scan_psb_and_decompile(self, scn_dir: str) -> PlainDict:
        ...
