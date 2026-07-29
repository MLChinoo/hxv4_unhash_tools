"""
从cglist.csv文件中获取cg缩略图thum及sd文件
"""

import csv

from plaintext_providers import register


@register(name="from_cglist_csv")
def collect(self, cglist_csv_filepath: str):
    with open(cglist_csv_filepath, mode="r", encoding="utf-16le") as f:
        cglist_csv = csv.reader(f)
        for row in cglist_csv:
            cg_filename = row[0].strip().lower()
            if cg_filename.startswith("#"):
                continue
            if ":" in cg_filename:
                print(f"bad cg_filename, ignored: {cg_filename} in {cglist_csv_filepath}")
                continue
            cg_name = cg_filename.replace("thum_", "")
            self.filename_plaintexts.update([
                # ev部分文件名迁移至from_imagediffmap_csv()
                f"{cg_filename}.jpg",
                f"{cg_filename}.png",
                f"{cg_filename}_censored.jpg",
                f"{cg_filename}_censored.png",
                f"{cg_filename}.psb",
                f"{cg_filename}_censored.psb"
            ])
            if cg_filename.startswith("thum_"):
                self.filename_plaintexts.update([
                    # savethum必定censored
                    f"save{cg_filename}.jpg",
                    f"save{cg_filename}.png",
                    f"save{cg_filename}.psb"
                ])
            # ev:
            if cg_filename.startswith("thum_ev"):
                for cg_diffs in row[1:]:
                    for cg_diff in cg_diffs.replace("*", "").split("|"):
                        if not cg_diff.startswith(cg_name):
                            print(f"bad cg_diff with cg_name, ignored: {cg_diff}, {cg_name}")
                            continue
                        cg_name_last_pos = cg_diff.find(cg_name) + len(cg_name)
                        for cg_diff_last_pos in range(cg_name_last_pos, len(cg_diff)+1):
                            filename = f"{cg_name}{cg_diff[cg_name_last_pos:cg_diff_last_pos]}"
                            self.filename_plaintexts.update([
                                f"{filename}.pimg",
                                f"{filename}_censored.pimg",
                                f"thum_{filename}.png",
                                f"thum_{filename}.jpg",
                                f"thum_{filename}_censored.png",
                                f"thum_{filename}_censored.jpg",
                                f"savethum_{filename}.png",
                                f"savethum_{filename}.jpg",
                                f"{filename}.psb",
                                f"{filename}_censored.psb",
                                f"thum_{filename}.psb",
                                f"thum_{filename}_censored.psb",
                                f"savethum_{filename}.psb",
                                f"{filename}.png"
                            ])
            # sd:
            if cg_filename.startswith("thum_sd"):  # thum_sd001
                sd_name = cg_filename[5:]  # sd001
                self.filename_plaintexts.update((
                    f"{sd_name}.mtn",
                    f"{sd_name}.psb"
                ))
                for sd_diff in row[1:]:
                    sd_diff = sd_diff.strip()  # sd001a01
                    self.filename_plaintexts.update((
                        f"{sd_diff}.jpg",
                        f"{sd_diff}.png",
                        f"{sd_diff}.asd",
                        f"{sd_diff}.psb"
                    ))
    return self
