# 此文件由 utils/generate_provider_typing.py 自动生成，请勿手动修改。
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from plain_dict import PlainDict


class PlainDictProviders:
    def duplicate_lower(self) -> PlainDict:
        ...

    def find_missing_voices(self, voice_dirs: Iterable, check_file_existence = False) -> PlainDict:
        ...

    def from_base_stage(self, base_stage_filepath: str, file_encoding: str) -> PlainDict:
        ...

    def from_bgv_csv(self, voice_dir, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_cglist_csv(self, cglist_csv_filepath: str, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_charvoice_csv(self, charvoice_csv_filepath, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_chthum_index_pbd(self, chthum_index_pbd_filepath) -> PlainDict:
        ...

    def from_cxdecextractor_logs(self, directory_hash_log_filepath: str, filename_hash_log_filepath: str, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_fgimage_pbd_files(self, fgimage_dir) -> PlainDict:
        ...

    def from_imagediffmap_csv(self, imagediffmap_csv_filepath, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_imagedressmap_txt(self, imagedressmap_txt_filepath, file_encoding: str) -> PlainDict:
        ...

    def from_imageevalmap_csv(self, imageevalmap_csv_filepath, file_encoding: str) -> PlainDict:
        ...

    def from_imagemulti_txt(self, imagemulti_txt_filepath, file_encoding: str) -> PlainDict:
        ...

    def from_imagenamemap_txt(self, imagenamemap_txt_filepath, file_encoding: str) -> PlainDict:
        ...

    def from_imagepropmap_txt(self, imagepropmap_txt_filepath, file_encoding: str) -> PlainDict:
        ...

    def from_krkrdump_logs(self, krkrdump_dir) -> PlainDict:
        ...

    def from_replay_ks(self, replay_ks_filepath, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_savelist_csv(self, savelist_csv_filepath, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_scenelist_csv(self, scenelist_csv_filepath, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_soundlist_csv(self, soundlist_csv_filepath, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def from_tlgref_files(self, tlgref_dir: str) -> PlainDict:
        ...

    def scan_fgimage_stands(self, fgimage_dir, file_encoding: str = 'utf-16le') -> PlainDict:
        ...

    def scan_psb_and_decompile(self, scn_dir: str) -> PlainDict:
        ...

    def scan_psb_and_decompile_enhanced(self, scn_dir: str, file_encoding: str = 'UTF-8') -> PlainDict:
        ...

    def scan_uipsd_multi_lang(self, uipsd_dir: str) -> PlainDict:
        ...

    def scan_uipsd_pbds(self, uipsd_dir: str) -> PlainDict:
        ...

    def scan_unobfuscated_directory(self, base_dir: str) -> PlainDict:
        ...
