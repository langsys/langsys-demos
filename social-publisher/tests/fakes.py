import json


class FakeResponse:
    def __init__(self, status: int = 200, body=None, headers: dict | None = None):
        self.status_code = status
        self._body = body
        self.headers = headers or {}
        self.content = b'' if body is None else json.dumps(body).encode()
        self.text = self.content.decode()

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    def json(self):
        return self._body


class FakeSession:
    """Answers each request with the first scripted response whose method and URL fragment match."""

    def __init__(self, script: list[tuple[str, str, FakeResponse]]):
        self.script = list(script)
        self.calls = []

    def request(self, method: str, url: str, **kwargs):
        self.calls.append((method, url, kwargs))
        for index, (wanted_method, fragment, response) in enumerate(self.script):
            if wanted_method == method and fragment in url:
                del self.script[index]
                return response
        raise AssertionError(f'unexpected request {method} {url}')

    def urls(self) -> list[str]:
        return [f'{method} {url}' for method, url, _ in self.calls]
