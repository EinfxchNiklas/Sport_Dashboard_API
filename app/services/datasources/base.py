import httpx


class BaseDataSource:
    def __init__(self, base_url: str, headers: dict | None = None, timeout: float = 15.0):
        self._client = httpx.Client(base_url=base_url, headers=headers or {}, timeout=timeout)

    def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        resp = self._client.get(path, params=params)
        resp.raise_for_status()
        return resp

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
