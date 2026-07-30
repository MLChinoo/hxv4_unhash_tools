import json
import pythonnet
from pathlib import Path
from config import Config
from typing import Optional

class _TjsParser:
    def __init__(self, config: Config):
        pythonnet.load("coreclr")

        import clr
        clr.AddReference(str(config.tjsparser_dll))

        from TjsParser import Parser
        from TjsParser.Serialization import AstJson

        self._parser = Parser
        self._ast_json = AstJson

    def parse(self, tjs_filepath: Path) -> str:
        tjs_filepath = Path(tjs_filepath).resolve()
        if not tjs_filepath.is_file():
            raise FileNotFoundError(tjs_filepath)

        parse_result = self._parser.ParseFile(str(tjs_filepath))
        return str(self._ast_json.Serialize(parse_result))

_tjs_parser: Optional[_TjsParser] = None

def initialize(config: Config) -> None:
    global _tjs_parser
    _tjs_parser = _TjsParser(config)

def parse(tjs_filepath: Path) -> str:
    if _tjs_parser is None:
        raise RuntimeError("TjsParser.dll is not initialized.")
    return _tjs_parser.parse(tjs_filepath)

def load(tjs_filepath: Path):
    return json.loads(parse(tjs_filepath))