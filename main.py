from pathlib import Path

from config import Config
from hxnames import add_missing_hashes, load_hxnames, save_hxnames
from plain_dict import PlainDict
from renamer import rename_hashed_items
from utils.krkr_hxv4_hash import set_hashlib


current_config = Config(
    project_dir=Path(__file__).resolve().parent,
    rename_dir=Path(r"C:\Users\MLChinoo\Desktop\3lj_data_full"),
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
        .scan_psb_and_decompile(
            r"C:\Users\MLChinoo\Desktop\3lj_data_full\scn"
        )
        # .from_base_stage(
        #     r"C:\Users\MLChinoo\Desktop\3lj_data_full\patch\base.stage"
        # )
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
    current_config.prepare()
    set_hashlib(current_config)

    dictionary = build_plain_dictionary()
    path_hash_map, file_hash_map = load_hxnames(
        current_config.hxnames_file
    )
    add_missing_hashes(dictionary, path_hash_map, file_hash_map)
    save_hxnames(
        current_config.hxnames_file,
        path_hash_map,
        file_hash_map,
    )
    rename_hashed_items(
        current_config.rename_dir,
        path_hash_map,
        file_hash_map,
    )


if __name__ == "__main__":
    main()
