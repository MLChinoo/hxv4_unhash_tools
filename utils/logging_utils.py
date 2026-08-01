import logging
from datetime import datetime
from pathlib import Path


class FilenameFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        prefix = f"[{record.filename}]"
        return "\n".join(f"{prefix}{line}" for line in message.splitlines())


def configure_logging() -> Path:
    logs_dir = Path.cwd() / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_filepath = logs_dir / datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")

    formatter = FilenameFormatter("%(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(log_filepath, encoding="UTF-8")
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[stream_handler, file_handler],
        force=True
    )
    return log_filepath
