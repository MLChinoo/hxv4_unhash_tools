"""
从systrans.ini文件中获取转场规则文件名
"""

from plaintext_providers import register


@register(name="from_systrans_ini")
def collect(self, systrans_ini_filepath, file_encoding: str):
    rules = set()
    with open(systrans_ini_filepath, mode="r", encoding=file_encoding) as f:
        content = f.read()
        for line in content.splitlines():
            line = line.strip().replace("\ufeff", "")
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            right_hand_side = line.split("=", 1)[1].strip()
            if right_hand_side.startswith("@") or right_hand_side.startswith("0:&"):
                continue
            for part in right_hand_side.split(":"):
                part = part.strip()
                if part and not part.isdigit() and not part.startswith("@"):
                    rules.add(part)

    count = 0
    for rule in rules:
        for extension in (".png", ".pimg", ".tlg", ".psb"):
            self.filename_plaintexts.add(f"{rule}{extension}")
        count += 1

    if count > 0:
        print(f"[systrans] 提取了 {count} 个转场规则名")
    return self
