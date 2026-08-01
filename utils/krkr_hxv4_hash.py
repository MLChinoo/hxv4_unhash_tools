import ctypes
import functools
from pathlib import Path
from typing import Optional

from config import Config

krkrhxv4hash_dll: Optional[ctypes.CDLL] = None

def set_hashlib(data):
    if isinstance(data, Path):
        global krkrhxv4hash_dll
        krkrhxv4hash_dll = ctypes.CDLL(str(data.resolve()))
        krkrhxv4hash_dll.get_filename_hash.argtypes = [ctypes.c_wchar_p]
        krkrhxv4hash_dll.get_filename_hash.restype = ctypes.POINTER(ctypes.c_uint8)
        krkrhxv4hash_dll.get_path_hash.argtypes = [ctypes.c_wchar_p]
        krkrhxv4hash_dll.get_path_hash.restype = ctypes.c_uint64
    elif isinstance(data, Config):
        set_hashlib(data.krkrhxv4hash_dll)
    else:
        raise TypeError(data)

def _require_dll(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if krkrhxv4hash_dll is None:
            raise RuntimeError("KrkrHxv4Hash.dll is not initialized.")
        return func(*args, **kwargs)
    return wrapper

def _str_to_utf16_ptr(s: str):
    utf16_bytes = s.encode("utf-16le") + b"\x00\x00"
    buf = ctypes.create_string_buffer(utf16_bytes)
    return ctypes.cast(buf, ctypes.c_wchar_p)

@_require_dll
def get_file_hash(filename: str) -> str:
    ptr = _str_to_utf16_ptr(filename)
    arr_ptr = krkrhxv4hash_dll.get_filename_hash(ptr)
    hash_result = ''.join(f"{arr_ptr[i]:02X}" for i in range(32))
    return hash_result

@_require_dll
def get_path_hash(pathname: str) -> str:
    ptr = _str_to_utf16_ptr(pathname)
    num = krkrhxv4hash_dll.get_path_hash(ptr)
    hash_result = f"{num:016X}"
    return hash_result

def is_file_hash(input: str) -> bool:
    return (
        len(input) == 64
        and all(char.lower() in "0123456789abcdef" for char in input)
    )

def is_path_hash(input: str) -> bool:
    return (
        len(input) == 16
        and all(char.lower() in "0123456789abcdef" for char in input)
    )

if __name__ == "__main__":
    set_hashlib(Path(r"C:\Users\MLChinoo\PycharmProjects\hxv4_unhash_tools\binaries\KrkrHxv4Hash.dll"))
    print(get_file_hash("macro_1.ks"))
