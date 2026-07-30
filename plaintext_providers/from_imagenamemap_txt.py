"""
从imagenamemap.txt文件中获取图片名和censored映射文件名
"""

from plaintext_providers import register


@register(name="from_imagenamemap_txt")
def collect(self, imagenamemap_txt_filepath, file_encoding: str = "utf-16le"):
    count = 0
    with open(imagenamemap_txt_filepath, mode="r", encoding=file_encoding) as f:
        content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            for part in parts:
                part = part.strip()
                if part and not part.startswith("_"):
                    for extension in (".pimg", ".tlg", ".png", ".psb"):
                        self.filename_plaintexts.update([
                            f"{part}{extension}",
                            f"{part}_censored{extension}"
                        ])
                    count += 1

    if count > 0:
        print(f"[imagenamemap] 提取了 {count} 个图片名")
    return self
