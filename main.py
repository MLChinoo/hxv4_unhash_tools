import os
import shutil
from pathlib import Path

from config import Config
from plain_dict import PlainDict
from utils.file_utils import get_unique_name, merge_dir
from utils.krkr_hxv4_hash import get_file_hash, get_path_hash, set_hashlib, is_path_hash, is_file_hash
import utils.tjs_parser


current_config = Config(
    project_dir=Path(__file__).resolve().parent,
    rename_dir=Path(r"D:\gals\dumps\lemonade_dumps"),
)

# 在这里添加明文字典来源；直接修改、添加或注释链式调用并填写参数。
def build_plain_dictionary():
    return (
        PlainDict(
            config=current_config,
            pathnames=[
                "/",
            ],
            filenames=[
                "base.stage",
                "cglist.csv",
                "soundlist.csv",
                "charvoice.csv",
                "imagediffmap.csv",
                "savelist.csv",
                "scenelist.csv",
                "replay.ks",
                "_chthum_index.pbd",
            ],
        )
        # .from_unobfuscated_directory(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data"
        # )
        # .scan_psb_and_decompile(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full\scn"
        # )
        .from_base_stage(
            r"D:\gals\dumps\lemonade_dumps\bgimage\base.stage"
        )
        # .from_cglist_csv(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full\patch\cglist.csv"
        # )
        # .from_soundlist_csv(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\data\main\soundlist.csv"
        # )
        # .add_char_sys_voices(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\data\main\charvoice.csv"
        # )
        # .from_imagediffmap_csv(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\patch\imagediffmap.csv"
        # )
        # .from_bgv_csv(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full\voice"
        # )
        # .from_savelist_csv(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\data\main\savelist.csv"
        # )
        # .from_scenelist_csv(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\data\main\scenelist.csv"
        # )
        # .from_krkrdump_logs(
        #     r"Z:\游戏存档\lllj krkrdump"
        # )
        # .find_missing_voices(
        #     [
        #         r"C:\Users\MLChinoo\Desktop\3lj_data_full\voice",
        #         r"C:\Users\MLChinoo\Desktop\3lj_data_full\voice2",
        #         r"C:\Users\MLChinoo\Desktop\3lj_data_full\patch",
        #     ]
        # )
        # .add_movies(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\data\scenario\replay.ks"
        # )
        # .from_stand_files(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full\fgimage"
        # )
        # .from_pbd_files(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full\fgimage"
        # )
        # .from_chthum_index_pbd(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full"
        #     r"\data\thum\chthum\_chthum_index.pbd"
        # )
        .duplicate_lower()
    )


def main():
    current_config.validate()
    set_hashlib(current_config)
    utils.tjs_parser.initialize(current_config)

    dictionary = build_plain_dictionary()

    path_hash_map = {}
    file_hash_map = {}
    if not current_config.hxnames_file.exists():
        current_config.hxnames_file.touch()

    with current_config.hxnames_file.open(
        mode="r",
        encoding="UTF-8",
    ) as h:
        for line in h.readlines():
            if line.strip() == "":
                continue
            assert len(splitted := line.replace("\n", "").split(":")) == 2, line
            hx_hash, hx_name = splitted
            if is_path_hash(hx_hash):  # path
                path_hash_map[hx_name] = hx_hash
            elif is_file_hash(hx_hash):  # file
                file_hash_map[hx_name] = hx_hash
            else:
                raise Exception(hx_hash)

    path_to_hash = (
        dictionary.pathname_plaintexts - set(path_hash_map.keys())
    )
    file_to_hash = (
        dictionary.filename_plaintexts - set(file_hash_map.keys())
    )

    print("新增hash：")
    for to_hash in (path_to_hash, file_to_hash):
        for item in to_hash:
            print(item)
    print()

    for pathname in path_to_hash:
        pathname = pathname.strip().replace("\ufeff", "")  # remove bom
        if pathname != "":
            assert "/" in pathname
        path_hash_map[pathname] = get_path_hash(pathname)

    for filename in file_to_hash:
        filename = filename.strip().replace("\ufeff", "")  # remove bom
        file_hash_map[filename] = get_file_hash(filename)

    with current_config.hxnames_file.open(
        mode="w",
        encoding="UTF-8",
    ) as h:
        for hash_map in (path_hash_map, file_hash_map):
            for name, hx_hash in hash_map.items():
                if name.strip() == "":
                    continue
                h.write(f"{hx_hash}:{name}\n")

    renamed_file_count = 0
    renamed_dir_count = 0
    hash_path_map = {
        value: key for key, value in path_hash_map.items()
    }
    hash_file_map = {
        value: key for key, value in file_hash_map.items()
    }

    for root, dirs, files in os.walk(
        current_config.rename_dir,
        topdown=False,
    ):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filename in hash_file_map.keys():
                new_name = hash_file_map[filename]
                new_path = os.path.join(root, new_name)
                new_path = get_unique_name(new_path)
                try:
                    os.rename(filepath, new_path)
                    renamed_file_count += 1
                    print(
                        "文件重命名成功: "
                        f"{Path(filepath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(new_path).relative_to(current_config.rename_dir)}"
                    )
                except Exception as error:
                    print(
                        "文件重命名失败: "
                        f"{Path(filepath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(new_path).relative_to(current_config.rename_dir)}，"
                        f"原因: {error}"
                    )

        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            if dirname in hash_path_map.keys():
                assert hash_path_map[dirname][-1] == "/"
                target_rel_path = hash_path_map[dirname].rstrip("/\\")
                dest_path = os.path.join(root, target_rel_path)

                parent_dir = os.path.dirname(dest_path)
                os.makedirs(parent_dir, exist_ok=True)

                try:
                    if os.path.exists(dest_path):
                        merge_dir(dirpath, dest_path)
                    else:
                        shutil.move(dirpath, dest_path)
                    renamed_dir_count += 1
                    print(
                        "目录重命名成功: "
                        f"{Path(dirpath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(dest_path).relative_to(current_config.rename_dir)}"
                    )
                except Exception as error:
                    print(
                        "目录重命名失败: "
                        f"{Path(dirpath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(dest_path).relative_to(current_config.rename_dir)}，"
                        f"原因: {error}"
                    )

    print(
        "重命名完成："
        f"共重命名文件 {renamed_file_count} 个，"
        f"目录 {renamed_dir_count} 个"
    )


if __name__ == "__main__":
    main()
