from pathlib import Path

from utils.krkr_hxv4_hash import get_file_hash, get_path_hash


def load_hxnames(filepath: Path):
    path_hash_map = {}
    file_hash_map = {}

    if not filepath.exists():
        filepath.touch()

    with filepath.open(mode="r", encoding="UTF-8") as h:
        h_lines = h.readlines()
        for line in h_lines:
            if line.strip() == "":
                continue
            assert len(splitted := line.replace("\n", "").split(":")) == 2, line
            hx_hash, hx_name = splitted
            if len(hx_hash) == 16:  # path
                path_hash_map[hx_name] = hx_hash
            elif len(hx_hash) == 64:  # file
                file_hash_map[hx_name] = hx_hash
            else:
                raise Exception(hx_hash)

    return path_hash_map, file_hash_map


def add_missing_hashes(dictionary, path_hash_map, file_hash_map):
    path_to_hash: set = (
        dictionary.pathname_plaintexts - set(path_hash_map.keys())
    )
    file_to_hash: set = (
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


def save_hxnames(filepath: Path, path_hash_map, file_hash_map):
    with filepath.open(mode="w", encoding="UTF-8") as h:
        for hash_map in (path_hash_map, file_hash_map):
            for name, hx_hash in hash_map.items():
                if name.strip() == "":
                    continue
                h.write(f"{hx_hash}:{name}\n")
