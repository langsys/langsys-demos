import os
import re
from pathlib import Path

from dotenv import load_dotenv


class MissingSetting(Exception):
    pass


def load(env_file: Path | None) -> Path:
    path = env_file or Path.cwd() / '.env'
    load_dotenv(path, override=True)
    return path


def require(*names: str) -> dict:
    values = {name: os.getenv(name, '').strip() for name in names}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise MissingSetting(f"missing in .env: {', '.join(missing)}")
    return values


def optional(name: str, default: str) -> str:
    return os.getenv(name, '').strip() or default


def upsert(path: Path, values: dict) -> None:
    """Set each key in the .env file, replacing its line or appending one."""
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    for name, value in values.items():
        line = f'{name}={value}'
        pattern = re.compile(rf'^{re.escape(name)}=.*$', re.M)
        if pattern.search(text):
            text = pattern.sub(lambda _: line, text)
        else:
            text = text + ('' if not text or text.endswith('\n') else '\n') + line + '\n'
    path.write_text(text, encoding='utf-8')
