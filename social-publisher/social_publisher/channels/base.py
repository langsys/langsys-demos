import time
from datetime import datetime, timezone

import requests

from ..post import Result

RETRIES = 3
MAX_WAIT = 60
IDEMPOTENT = ('GET', 'PUT', 'DELETE')


class ApiError(Exception):
    pass


def call(session, channel: str, method: str, url: str, sleep=time.sleep, retry: bool | None = None, **kwargs):
    """Send a request, waiting out a rate limit and, when the request is safe to repeat, a server error or dropped connection.

    A POST is only repeated on a rate limit (the request was refused, so nothing
    happened) unless `retry` says it is safe, as for a numbered upload chunk.
    """
    kwargs.setdefault('timeout', 120)
    repeatable = method in IDEMPOTENT if retry is None else retry
    for attempt in range(RETRIES + 1):
        try:
            response = session.request(method, url, **kwargs)
        except (requests.ConnectionError, requests.Timeout) as error:
            if not repeatable or attempt == RETRIES:
                raise ApiError(f'{channel} {method} {url} failed: {error}') from error
            sleep(2 ** (attempt + 1))
            continue
        if response.ok:
            return response
        wait = _wait(response, attempt, repeatable)
        if wait is None or attempt == RETRIES:
            raise ApiError(f'{channel} {method} {url} returned {response.status_code}: {response.text[:500]}{_reset_note(response)}')
        sleep(wait)


def body(response) -> dict:
    return response.json() if response.content else {}


def step(result: Result, name: str, action) -> None:
    """Run a follow-up to a post that already went up; a failure becomes a warning, not a failed post."""
    try:
        action()
    except Exception as error:
        result.warnings.append(f'{name}: {error}')


def _wait(response, attempt: int, repeatable: bool) -> float | None:
    if response.status_code == 429:
        wait = _rate_limit_wait(response)
        return wait if wait <= MAX_WAIT else None
    if response.status_code >= 500 and repeatable:
        return 2 ** (attempt + 1)
    return None


def _rate_limit_wait(response) -> float:
    retry_after = response.headers.get('retry-after')
    if retry_after and retry_after.isdigit():
        return float(retry_after)
    reset = response.headers.get('x-rate-limit-reset')
    if reset and reset.isdigit():
        return max(0.0, int(reset) - time.time())
    return 5.0


def _reset_note(response) -> str:
    reset = response.headers.get('x-rate-limit-reset')
    if response.status_code != 429 or not (reset and reset.isdigit()):
        return ''
    return f" (the limit resets at {datetime.fromtimestamp(int(reset), timezone.utc):%Y-%m-%d %H:%M} UTC)"
