"""
从cglist.csv文件中获取cg缩略图thum及sd文件
"""

import csv

from plaintext_providers import register


@register(name="from_cglist_csv")
def collect(self, cglist_csv_filepath: str, file_encoding: str):
    count = 0
    with open(cglist_csv_filepath, mode="r", encoding=file_encoding) as f:
        cglist_csv = csv.reader(f)
        for row in cglist_csv:
            if len(row) == 0:
                continue
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
                f"{cg_filename}_censored.psb",
                f"{cg_filename}.tlg",
                f"{cg_filename}_censored.tlg",
                f"{cg_filename}.pimg",
                f"{cg_filename}_censored.pimg",
                f"{cg_name}.tlg",
                f"{cg_name}.png",
                f"{cg_name}.pimg",
                f"{cg_name}_censored.tlg",
                f"{cg_name}_censored.png",
                f"{cg_name}_censored.pimg"
            ])
            count += 1
            if cg_filename.startswith("thum_"):
                self.filename_plaintexts.update([
                    # savethum必定censored
                    f"save{cg_filename}.jpg",
                    f"save{cg_filename}.png",
                    f"save{cg_filename}.psb",
                    f"save{cg_filename}.tlg"
                ])
            # ev:
            if cg_filename.startswith("thum_ev"):
                for cg_diffs in row[1:]:
                    for cg_diff in cg_diffs.replace("*", "").split("|"):
                        cg_diff = cg_diff.strip().replace("\t", "")
                        if not cg_diff.startswith(cg_name):
                            print(f"bad cg_diff with cg_name, ignored: {cg_diff}, {cg_name}")
                            continue
                        cg_name_last_pos = cg_diff.find(cg_name) + len(cg_name)
                        for cg_diff_last_pos in range(cg_name_last_pos, len(cg_diff)+1):
                            filename = f"{cg_name}{cg_diff[cg_name_last_pos:cg_diff_last_pos]}"
                            for locale_suffix in ("", "_en", "_cn", "_tw"):
                                self.filename_plaintexts.update([
                                    f"{filename}{locale_suffix}.pimg",
                                    f"{filename}{locale_suffix}_censored.pimg",
                                    f"{filename}{locale_suffix}.tlg",
                                    f"{filename}{locale_suffix}_censored.tlg",
                                    f"{filename}{locale_suffix}.psb",
                                    f"{filename}{locale_suffix}_censored.psb",
                                    f"{filename}{locale_suffix}.png",
                                    f"{filename}{locale_suffix}_censored.png"
                                    
                                    f"thum_{filename}{locale_suffix}.png",
                                    f"thum_{filename}{locale_suffix}_censored.png",
                                    f"thum_{filename}{locale_suffix}.jpg",
                                    f"thum_{filename}{locale_suffix}_censored.jpg",
                                    f"thum_{filename}{locale_suffix}.psb",
                                    f"thum_{filename}{locale_suffix}_censored.psb",
                                    f"thum_{filename}{locale_suffix}.tlg",
                                    f"thum_{filename}{locale_suffix}_censored.tlg",
                                    
                                    f"savethum_{filename}{locale_suffix}.png",
                                    f"savethum_{filename}{locale_suffix}.jpg",
                                    f"savethum_{filename}{locale_suffix}.psb",
                                    f"savethum_{filename}{locale_suffix}.tlg",
                                ])
            # sd:
            if cg_filename.startswith("thum_sd"):  # thum_sd001
                sd_name = cg_filename[5:]  # sd001
                self.filename_plaintexts.update((
                    f"{sd_name}.mtn",
                    f"{sd_name}.psb",
                    f"{sd_name}.tlg"
                ))
                for sd_diff in row[1:]:
                    sd_diff = sd_diff.strip().replace("\t", "")  # sd001a01
                    if sd_diff == "":
                        continue
                    for locale_suffix in ("", "_en", "_cn", "_tw"):
                        self.filename_plaintexts.update((
                            f"{sd_diff}{locale_suffix}.jpg",
                            f"{sd_diff}{locale_suffix}.png",
                            f"{sd_diff}{locale_suffix}.tlg",
                            f"{sd_diff}{locale_suffix}.pimg",
                            f"{sd_diff}{locale_suffix}.asd",
                            f"{sd_diff}{locale_suffix}.psb",
                            f"{sd_diff}{locale_suffix}_censored.jpg",
                            f"{sd_diff}{locale_suffix}_censored.png",
                            f"{sd_diff}{locale_suffix}_censored.tlg",
                            f"{sd_diff}{locale_suffix}_censored.pimg"
                        ))
    print(f"[cglist.csv] 提取了 {count} 个 CG 条目")
    return self
