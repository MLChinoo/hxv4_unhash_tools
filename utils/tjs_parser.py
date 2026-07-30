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
        from TjsParser.Parsing import ParseOptions
        from TjsParser.Serialization import AstJson

        self._parser = Parser
        self._parse_options = ParseOptions
        self._ast_json = AstJson

    def parse(self, tjs_filepath: Path, file_encoding: str) -> str:
        tjs_filepath = Path(tjs_filepath).resolve()
        if not tjs_filepath.is_file():
            raise FileNotFoundError(tjs_filepath)

        parse_options = self._parse_options()
        parse_options.EncodingHint = file_encoding
        parse_result = self._parser.ParseFile(
            str(tjs_filepath),
            parse_options
        )
        return str(self._ast_json.Serialize(parse_result))

_tjs_parser: Optional[_TjsParser] = None

def initialize(config: Config) -> None:
    global _tjs_parser
    _tjs_parser = _TjsParser(config)

def parse(tjs_filepath: Path, file_encoding: str) -> str:
    if _tjs_parser is None:
        raise RuntimeError("TjsParser.dll is not initialized.")
    return _tjs_parser.parse(tjs_filepath, file_encoding)

def load(tjs_filepath: Path, file_encoding: str):
    return json.loads(parse(tjs_filepath, file_encoding))
