"""
检查给定目录下未混淆文件名和目录名占全部文件名和目录名的百分比

即反混淆进度
"""
import os

from krkr_hxv4_hash import is_path_hash, is_file_hash

def get_progress_percent(root_dir: str) -> float:
    total_path = 0
    total_file = 0
    hashed_path = 0
    hashed_file = 0
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            total_path += 1
            if is_path_hash(d):
                hashed_path += 1
        for file in files:
            if file == "2EA4AAEC6A09F9D17E2A5A7AC422FB64B6A42195C55CF6772FB30C0FA0120C8D":
                # 未知文件，与游戏无关，疑似为GARbro提取时的bug
                continue
            total_file += 1
            if is_file_hash(file):
                hashed_file += 1
    return 1 - (hashed_path + hashed_file) / (total_path + total_file)

if __name__ == "__main__":
    print(f"{100 * get_progress_percent(r"C:\Users\MLChinoo\Desktop\3lj_data_full")}%")
