import logging
import os
import shutil
from pathlib import Path

from config import Config
from plain_dict import PlainDict
from utils.file_utils import get_unique_name, merge_dir
from utils.krkr_hxv4_hash import get_file_hash, get_path_hash, set_hashlib, is_path_hash, is_file_hash
from utils.logging_utils import configure_logging
import utils.tjs_parser


logger = logging.getLogger(__name__)


current_config = Config(
    project_dir=Path(__file__).resolve().parent,
    rename_dir=Path(r"D:\gals\dumps\dracu_dumps"),
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
                "charvoice.csv",
                "sysse.ini",
                "_chthum_index.pbd",
                "filegain.csv",
                "imagediffmap.csv",
                "imagedressmap.txt",
                "imageevalmap.csv",
                "imagemulti.txt",
                "imagenamemap.txt",
                "imagepropmap.txt",
                "replay.ks",
                "savelist.csv",
                "scenelist.csv",
                "soundgain.csv",
                "soundlist.csv",
                "systrans.ini",
            ],
        )
        ## ==================== 第一轮：无需依赖本工具上一轮重命名结果 ====================
        ## 从已经含有明文名称的目录树收集文件名和路径名，适合未加密版本、体验版或已部分还原的目录。
        .scan_unhashed_directory(
            base_dir=r"D:\gals\dumps\dracu_dumps"
        )
        ## 从 KrkrDump 的运行日志中读取目录名和文件名。
        #.from_krkrdump_logs(
        #    krkrdump_dir=r"D:\game\krkrdump_logs"
        #)
        ## 从 CxdecExtractor 的两个运行日志中分别读取目录名和文件名。
        #.from_cxdecextractor_logs(
        #    directory_hash_log_filepath=r"D:\gals\Dracu-Riot 脱steam\StringHashDumper_Output\DirectoryHash.log",
        #    filename_hash_log_filepath=r"D:\gals\Dracu-Riot 脱steam\StringHashDumper_Output\FileNameHash.log"
        #)
        ## 按文件头扫描 .ks.scn 场景文件，反编译后使用结构化字段提取语音、图片、脚本等明文名称。
        #.scan_psb_and_decompile(
        #    scn_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output"
        #)
        ## 与上一项使用相同反编译准备流程，但通过正则表达式提取更广泛的引用；可按游戏情况二选一或同时使用。
        #.scan_psb_and_decompile_re(
        #    scn_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output"
        #)
        ## 按文件头扫描 TLGref 立绘文件，并从二进制头部提取被引用的 TLG 文件名。
        #.scan_evimage_tlgrefs(
        #    evimage_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output"
        #)
        ### 按文件头扫描 uipsd PBD，提取 uipsd TLG文件名。
        #.scan_uipsd_pbds(
        #    uipsd_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\uipsd"
        #)
#
        ## ==================== 第二轮：完成第一轮重命名后 ====================
        ## 解析已重命名的 base.stage，生成背景图片及其缩略图。
        #.from_base_stage(
        #    base_stage_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\bgimage\base.stage",
        #    file_encoding="utf-16le"
        #)
        ## 解析已重命名的 cglist.csv，生成 CG 及 SD 的图片文件名及其缩略图和存档缩略图。
        #.from_cglist_csv(
        #    cglist_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\cglist.csv",
        #    file_encoding="utf-16le"
        #)
        ## 联合 charvoice.csv 与 sysse.ini，为每个角色前缀组合其系统语音。
        #.add_char_sys_voices(
        #    charvoice_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\charvoice.csv",
        #    sysse_ini_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\sysse.ini",
        #    file_encoding="utf-16le"
        #)
        ## 解析已重命名的 _chthum_index.pbd，提取角色缩略图文件名（多用于立绘鉴赏中）。
        #.from_chthum_index_pbd(
        #    chthum_index_pbd_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\upgrade\_chthum_index.pbd"
        #)
        ## 从 filegain.csv 提取部分音效名及背景音乐名。
        #.from_filegain_csv(
        #    filegain_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\filegain.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 imagediffmap.csv 提取部分 CG 差分名及其存档缩略图。
        #.from_imagediffmap_csv(
        #    imagediffmap_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\imagediffmap.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 imagedressmap.txt 提取部分立绘 .stand 文件名。
        #.from_imagedressmap_txt(
        #    imagedressmap_txt_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\imagedressmap.txt",
        #    file_encoding="utf-16le"
        #)
        ## 从 imageevalmap.csv 提取部分 CG 差分名。
        #.from_imageevalmap_csv(
        #    imageevalmap_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\imageevalmap.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 imagemulti.txt 提取部分角色立绘名。
        #.from_imagemulti_txt(
        #    imagemulti_txt_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\imagemulti.txt",
        #    file_encoding="utf-16le"
        #)
        ## 从 imagenamemap.txt 提取部分 CG 名。
        #.from_imagenamemap_txt(
        #    imagenamemap_txt_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\imagenamemap.txt",
        #    file_encoding="utf-16le"
        #)
        ## 从 imagepropmap.txt 提取部分资源名（多为剧情中使用的演出资源等）。
        #.from_imagepropmap_txt(
        #    imagepropmap_txt_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\imagepropmap.txt",
        #    file_encoding="utf-16le"
        #)
        ## 从 replay.ks 提取 OP / ED 视频文件名。
        #.from_replay_ks(
        #    replay_ks_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\scenario\replay.ks",
        #    file_encoding="utf-16le"
        #)
        ## 从 savelist.csv 提取存档缩略图及对应普通缩略图候选。
        #.from_savelist_csv(
        #    savelist_csv_filepath=r"D:\game\Extractor_Output\data\savelist.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 scenelist.csv 生成场景鉴赏缩略图。
        #.from_scenelist_csv(
        #    scenelist_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\scenelist.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 soundgain.csv 提取可能的音效名。
        #.from_soundgain_csv(
        #    soundgain_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\soundgain.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 soundlist.csv 提取背景音乐名。
        #.from_soundlist_csv(
        #    soundlist_csv_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\soundlist.csv",
        #    file_encoding="utf-16le"
        #)
        ## 从 systrans.ini 提取转场图片名。
        #.from_systrans_ini(
        #    systrans_ini_filepath=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\main\systrans.ini",
        #    file_encoding="utf-16le"
        #)
        ## 扫描第一轮由 SCN 引用并重命名出的 bgv*.csv，生成背景语音候选。
        #.scan_bgv_csv(
        #    voice_dir=r"D:\game\Extractor_Output\voice",
        #    file_encoding="utf-16le"
        #)
        ## 扫描第一轮由 SCN 引用并重命名出的 .stand，生成角色 PBD 和 sinfo。
        #.scan_fgimage_stands(
        #    fgimage_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output",
        #    file_encoding="utf-16le"
        #)
#
        ## ==================== 第三轮：完成第二轮重命名后 ====================
        ## 扫描由 scan_fgimage_stands 得到并重命名的角色 PBD，提取其中的 TLG/PNG 图层名。
        #.scan_fgimage_pbds(
        #    fgimage_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output"
        #)
        ## 根据已经重命名的文件的 cn/en/tw/jp 地区版本推导其它地区版本。
        #.scan_locale_files(
        #    locale_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\locale"
        #)
        ## 扫描已经重命名的未编译/已反编译 TJS 脚本字符串，提取更多文件引用；发现新 TJS 后可继续重复本轮。
        ## 不建议使用
        #.scan_tjs_scripts_re(
        #    tjs_dir=r"D:\game\Extractor_Output\data",
        #    file_encoding="utf-16le"
        #)
        ## 根据已重命名的 uipsd PBD/TLG 推导各地区与 pack/bg 变体；可与 scan_uipsd_pbds 交替多轮运行。
        #.scan_uipsd_multi_lang(
        #    uipsd_dir=r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\data\uipsd"
        #)
#
        ## ==================== 第四轮：其余来源基本完成后 ====================
        ## 根据已收集的语音编号序列推测缺号语音。
        #.scan_missing_voices(
        #    voice_dirs=[
        #        r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\voice",
        #        r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\upgrade2",
        #        r"D:\gals\Dracu-Riot 脱steam\Extractor_Output\adult"
        #    ],
        #    check_file_existence=True
        #)

        # 最后为当前收集到的所有路径名和文件名补充小写副本。
        .duplicate_lower()
    )


def main():
    configure_logging()
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

    logger.info("新增hash：")
    for to_hash in (path_to_hash, file_to_hash):
        for item in to_hash:
            logger.info(item)

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
                    logger.info(
                        "文件重命名成功: "
                        f"{Path(filepath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(new_path).relative_to(current_config.rename_dir)}"
                    )
                except Exception as error:
                    logger.error(
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
                    logger.info(
                        "目录重命名成功: "
                        f"{Path(dirpath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(dest_path).relative_to(current_config.rename_dir)}"
                    )
                except Exception as error:
                    logger.error(
                        "目录重命名失败: "
                        f"{Path(dirpath).relative_to(current_config.rename_dir)}"
                        " -> "
                        f"{Path(dest_path).relative_to(current_config.rename_dir)}，"
                        f"原因: {error}"
                    )

    logger.info(
        "重命名完成："
        f"共重命名文件 {renamed_file_count} 个，"
        f"目录 {renamed_dir_count} 个"
    )


if __name__ == "__main__":
    main()
