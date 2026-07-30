"""
从imagepropmap.txt文件中获取特殊资源文件名
"""
from itertools import product

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="from_imagepropmap_txt")
def collect(self: PlainDict, imagepropmap_txt_filepath, file_encoding: str):
    with open(imagepropmap_txt_filepath, mode="r", encoding=file_encoding) as f:
        content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            resource_name = parts[0].strip()
            resource_names = set()
            extensions = {".pimg", ".tlg", ".png", ".psb", ".mtn", ".wmv", ".stand"}
            if not resource_name:
                continue
            if "." in resource_name:
                resource_name, new_extension = resource_name.split(".", maxsplit=1)
                extensions.add(f".{new_extension}")
            resource_names.add(resource_name)

            if len(resource_names) != 0:
                for name, extension in product(resource_names, extensions):
                    self.filename_plaintexts.add(f"{name}{extension}")
    return self
