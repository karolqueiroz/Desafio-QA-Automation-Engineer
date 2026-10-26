import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.config import API_BASE_URL, API_TIMEOUT

logger = logging.getLogger("api")


class BaseClient:
    """Sessão HTTP compartilhada, com timeout, retry e log das chamadas."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        # Retry apenas em métodos idempotentes (GET) para falhas de gateway,
        # evitando duplicar POSTs (ex.: criação de usuário).
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def request(self, method: str, path: str, token: str | None = None, **kwargs):
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"
        url = f"{self.base_url}{path}"
        response = self.session.request(
            method, url, headers=headers, timeout=API_TIMEOUT, **kwargs
        )
        logger.info("%s %s -> %s", method, url, response.status_code)
        return response
