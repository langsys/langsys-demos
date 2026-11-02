import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture
def files(tmp_path):
    def make(name: str, size: int = 10) -> Path:
        path = tmp_path / name
        path.write_bytes(b'x' * size)
        return path
    return make
