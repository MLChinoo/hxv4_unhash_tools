import os
import shutil
from pathlib import Path

from utils.file_utils import get_unique_name, merge_dir


def rename_hashed_items(rename_dir, path_hash_map, file_hash_map):
    renamed_file_count = 0
    renamed_dir_count = 0
    hash_path_map = {value: key for key, value in path_hash_map.items()}
    hash_file_map = {value: key for key, value in file_hash_map.items()}

    for root, dirs, files in os.walk(rename_dir, topdown=False):
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
                        f"{Path(filepath).relative_to(rename_dir)} -> "
                        f"{Path(new_path).relative_to(rename_dir)}"
                    )
                except Exception as error:
                    print(
                        "文件重命名失败: "
                        f"{Path(filepath).relative_to(rename_dir)} -> "
                        f"{Path(new_path).relative_to(rename_dir)}，"
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
                        f"{Path(dirpath).relative_to(rename_dir)} -> "
                        f"{Path(dest_path).relative_to(rename_dir)}"
                    )
                except Exception as error:
                    print(
                        "目录重命名失败: "
                        f"{Path(dirpath).relative_to(rename_dir)} -> "
                        f"{Path(dest_path).relative_to(rename_dir)}，"
                        f"原因: {error}"
                    )

    print(
        "重命名完成："
        f"共重命名文件 {renamed_file_count} 个，"
        f"目录 {renamed_dir_count} 个"
    )
    return renamed_file_count, renamed_dir_count
