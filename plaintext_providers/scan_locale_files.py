"""
从给定目录中已命名的locale文件获取其他语言变体文件名
"""

from pathlib import Path

from plain_dict import PlainDict
from plaintext_providers import register
from utils.krkr_hxv4_hash import is_file_hash


@register(name="scan_locale_files")
def collect(self: PlainDict, locale_dir: str):
    locale_suffixes = ["", "_cn", "_en", "_tw", "_jp"]
    locale_bases = set()
    for child in Path(locale_dir).rglob("*"):
        if not child.is_file() or is_file_hash(child.name):
            continue
        for locale_suffix in locale_suffixes:
            locale_suffix_index = child.name.rfind(locale_suffix + ".")
            if locale_suffix_index != -1:
                base_name = child.name[:locale_suffix_index]
                extension = child.name[locale_suffix_index + len(locale_suffix):]
                locale_bases.add((base_name, extension))
                break
            locale_suffix_index = child.name.rfind(locale_suffix)
            if locale_suffix_index != -1 and locale_suffix_index == len(child.name) - len(locale_suffix):
                base_name = child.name[:locale_suffix_index]
                locale_bases.add((base_name, ""))
                break

    for base_name, extension in locale_bases:
        for locale_suffix in locale_suffixes:
            filename = f"{base_name}{locale_suffix}{extension}"
            self.filename_plaintexts.add(filename)
    return self
