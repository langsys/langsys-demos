import mimetypes
from dataclasses import dataclass
from pathlib import Path

mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('video/mp4', '.m4v')

KINDS = {
    'image/jpeg':      'image',
    'image/png':       'image',
    'image/webp':      'image',
    'image/gif':       'gif',
    'video/mp4':       'video',
    'video/quicktime': 'video',
    'video/webm':      'video',
}


@dataclass(frozen=True)
class Media:
    path: Path
    mime: str
    kind: str
    size: int


def inspect(path: Path) -> Media:
    if not path.is_file():
        raise ValueError(f'{path}: file not found')
    mime = mimetypes.guess_type(path.name)[0] or ''
    if mime not in KINDS:
        raise ValueError(f"{path.name}: unsupported file type {mime or path.suffix!r} (use {', '.join(sorted(KINDS))})")
    return Media(path, mime, KINDS[mime], path.stat().st_size)


def inspect_all(paths: list[Path], problems: list[str]) -> list[Media]:
    found = []
    for path in paths:
        try:
            found.append(inspect(path))
        except ValueError as error:
            problems.append(str(error))
    return found


def megabytes(size: int) -> str:
    return f'{size / 1024 / 1024:.1f} MB'
