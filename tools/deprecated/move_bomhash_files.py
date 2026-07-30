"""
遍历目录并将"94D4A97C61498621"目录下的文件移动至上一层级目录

"94D4A97C61498621"应为根目录，即目录里的文件应在上一级目录下，而不是错误地新开一个目录
"""
import os
import shutil

from utils.file_utils import get_unique_name


def move_bomhash_files(root_dir):
    for current_dir, dirs, files in os.walk(root_dir, topdown=False):
        if "94D4A97C61498621" in dirs:
            target_path = os.path.join(current_dir, "94D4A97C61498621")
            print(f"处理目录: {target_path}")

            # 遍历目标子目录中的所有文件和文件夹
            for item in os.listdir(target_path):
                src = os.path.join(target_path, item)
                dest = os.path.join(current_dir, item)

                # 如果目标位置已存在，则重命名
                if os.path.exists(dest):
                    dest = get_unique_name(dest)

                shutil.move(src, dest)
                print(f"移动: {src} -> {dest}")

            # 删除空目录
            shutil.rmtree(target_path)
            print(f"已删除目录: {target_path}")

if __name__ == "__main__":
    root_directory = r"C:\Users\MLChinoo\Desktop\3lj_data_full"  # 替换为你的实际路径
    move_bomhash_files(root_directory)
