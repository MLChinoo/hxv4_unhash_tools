from pathlib import Path


class Config:
    def __init__(self, project_dir, rename_dir):
        self.project_dir = Path(project_dir).resolve()
        self.rename_dir = Path(rename_dir)

        binaries_dir = self.project_dir / "binaries"
        self.psbdecompile_exe = (
            binaries_dir / "psb_decompile" / "PsbDecompile.exe"
        )
        self.pbd2json_exe = binaries_dir / "pbd2json.exe"
        self.krkrhxv4hash_dll = binaries_dir / "KrkrHxv4Hash.dll"

        self.temp_dir = self.project_dir / "temp"
        self.psb_type_cache_pkl = self.temp_dir / "psb_type_cache.pkl"
        self.hxnames_file = self.project_dir / "HxNames.lst"

    def prepare(self):
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def validate(self):
        if not self.rename_dir.is_dir():
            raise FileNotFoundError(f"待处理目录不存在：{self.rename_dir}")
        if not self.krkrhxv4hash_dll.is_file():
            raise FileNotFoundError(
                f"哈希 DLL 不存在：{self.krkrhxv4hash_dll}"
            )
