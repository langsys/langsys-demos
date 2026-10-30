from dataclasses import asdict, dataclass, field, fields, replace
from pathlib import Path

from . import utm

CHANNELS = ('youtube', 'x', 'linkedin')
PREVIEW_LINKS = {
    'youtube':  'https://youtu.be/xxxxxxxxxxx',
    'x':        'https://x.com/i/status/0000000000000000000',
    'linkedin': 'https://www.linkedin.com/feed/update/urn:li:share:0000000000000000000/',
}


@dataclass
class Post:
    text: str = ''
    media: list[Path] = field(default_factory=list)
    title: str | None = None
    comment: str | None = None
    tags: list[str] = field(default_factory=list)
    privacy: str = 'public'
    publish_at: str | None = None
    thumbnail: Path | None = None
    playlist: str | None = None
    category: str = '28'
    alt_text: list[str] = field(default_factory=list)
    utm: dict | bool | None = None

    @classmethod
    def from_dict(cls, data: dict, base_dir: Path) -> 'Post':
        known = {item.name for item in fields(cls)}
        unknown = sorted(set(data) - known)
        if unknown:
            raise ValueError(f"unknown post field(s): {', '.join(unknown)}")
        values = dict(data)
        media = values.get('media', [])
        values['media'] = [_resolve(path, base_dir) for path in ([media] if isinstance(media, str) else media)]
        if values.get('thumbnail'):
            values['thumbnail'] = _resolve(values['thumbnail'], base_dir)
        if isinstance(values.get('tags'), str):
            values['tags'] = [tag.strip() for tag in values['tags'].split(',') if tag.strip()]
        if isinstance(values.get('alt_text'), str):
            values['alt_text'] = [values['alt_text']]
        return cls(**values)

    def tagged(self, source: str) -> 'Post':
        """The post with campaign tags on its links, utm_source being the channel it goes to."""
        settings = utm.tagging(self.utm)
        if not settings:
            return self
        comment = utm.tag_all(self.comment, source, settings) if self.comment else self.comment
        return replace(self, text=utm.tag_all(self.text, source, settings), comment=comment)

    def linked(self, links: dict) -> 'Post':
        """The post with each {youtube}, {x} or {linkedin} replaced by that channel's link from this run."""
        return replace(self, text=_fill(self.text, links), comment=_fill(self.comment, links) if self.comment else self.comment)

    def placeholders(self) -> list[str]:
        written = f'{self.text}\n{self.comment or ""}'
        return [channel for channel in CHANNELS if f'{{{channel}}}' in written]


@dataclass
class Result:
    channel: str
    ok: bool
    id: str | None = None
    url: str | None = None
    comment_url: str | None = None
    error: str | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _resolve(path: str | Path, base_dir: Path) -> Path:
    path = Path(path).expanduser()
    return path if path.is_absolute() else (base_dir / path).resolve()


def _fill(text: str, links: dict) -> str:
    for channel in CHANNELS:
        placeholder = f'{{{channel}}}'
        if placeholder in text:
            if channel not in links:
                raise ValueError(f'needs the {channel} link, but nothing was posted to {channel} before it in this run')
            text = text.replace(placeholder, links[channel])
    return text
