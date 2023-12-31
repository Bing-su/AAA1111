import asyncio
from pathlib import Path
from typing import Any, Mapping, Optional, Union

from beartype import beartype
from httpx import URL, AsyncClient, BasicAuth, Client, Timeout

from aaa1111.utils import load_from_file

from .action import ActionMixin
from .extras import ExtrasMixin
from .info import InfoMixin
from .options import OptionsMixin
from .toimg import ToImageMixin


@beartype
class AAA1111(OptionsMixin, InfoMixin, ActionMixin, ExtrasMixin, ToImageMixin):
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 7860,
        base_url: Optional[str] = None,
        https: bool = False,
        username: Union[str, bytes, None] = None,
        password: Union[str, bytes, None] = None,
        defaults: Union[str, Path, Mapping[str, Any], None] = None,
        client_kwargs: Optional[Mapping[str, Any]] = None,
    ):
        if base_url is None:
            pre = "https" if https else "http"
            init_base_url = f"{pre}://{host}:{port}"
        else:
            init_base_url = base_url

        if isinstance(defaults, (str, Path)):
            self.defaults = load_from_file(defaults)
        else:
            self.defaults = defaults or {}

        auth = BasicAuth(username, password) if username else None
        kwargs = {
            "auth": auth,
            "follow_redirects": True,
            "base_url": init_base_url,
            "timeout": None,
            **(client_kwargs or {}),
        }
        self.client = Client(**kwargs)
        self.aclient = AsyncClient(**kwargs)

        self.get = self.client.get
        self.aget = self.aclient.get
        self.post = self.client.post
        self.apost = self.aclient.post

    def __del__(self):
        self.client.close()
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            loop.create_task(self.aclient.aclose())
        else:
            asyncio.run(self.aclient.aclose())

    @property
    def base_url(self) -> URL:
        return self.client.base_url

    @base_url.setter
    def base_url(self, url: Union[str, URL]):
        self.client.base_url = url
        self.aclient.base_url = url

    @property
    def timeout(self) -> Timeout:
        return self.client.timeout

    @timeout.setter
    def timeout(self, timeout: Any):
        self.client.timeout = timeout
        self.aclient.timeout = timeout
