"""
将GARBro提取出的文件根据文件名还原目录结构

有时GARBro提取时并没有遵循原有目录结构，而是全部放在一个目录中，并将目录结构表示在文件名里，
例如94D4A97C61498621_00A93384A021B7BEC8FF4E8993126ABC11AE9473B411D1893594DC96271F219E，
需还原为94D4A97C61498621/00A93384A021B7BEC8FF4E8993126ABC11AE9473B411D1893594DC96271F219E
CxdecExtractor提取则无此问题
"""
import os
import shutil

def restore_dir_structure(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and '_' in filename:
            name_part, ext = os.path.splitext(filename)
            parts = name_part.split('_')

            target_dir = os.path.join(folder_path, *parts[:-1])
            os.makedirs(target_dir, exist_ok=True)

            new_file_path = os.path.join(target_dir, parts[-1] + ext)

            shutil.move(file_path, new_file_path)
            print(f"移动：{file_path} -> {new_file_path}")

if __name__ == "__main__":
    root_dir = r"C:\Users\MLChinoo\Desktop\3lj_data_full"
    for dir in os.listdir(root_dir):
        folder = os.path.join(root_dir, dir)
        print(folder)
        restore_dir_structure(folder)
