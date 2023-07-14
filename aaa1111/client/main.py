import asyncio
import platform
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

from beartype import beartype
from httpx import AsyncClient, BasicAuth, Client

from aaa1111.utils import aload_dict_file, load_dict_file

from .toimg import ToImageMixin

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@beartype
class AAA1111(ToImageMixin):
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
            self.defaults = load_dict_file(defaults)
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
    def base_url(self):
        return self.client.base_url

    @base_url.setter
    def base_url(self, url: str):
        self.client.base_url = url
        self.aclient.base_url = url

    @staticmethod
    def _get_payload(payload: Any) -> Dict[str, Any]:
        if hasattr(payload, "asdict"):
            return payload.asdict()
        if is_dataclass(payload):
            return asdict(payload)
        if isinstance(payload, (str, Path)):
            return load_dict_file(payload)
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, Mapping):
            return dict(payload)
        msg = f"Unsupported payload type: {type(payload)}"
        raise ValueError(msg)

    @staticmethod
    async def _aget_payload(payload: Any) -> Dict[str, Any]:
        if hasattr(payload, "asdict"):
            return payload.asdict()
        if is_dataclass(payload):
            return asdict(payload)
        if isinstance(payload, (str, Path)):
            return await aload_dict_file(payload)
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, Mapping):
            return dict(payload)
        msg = f"Unsupported payload type: {type(payload)}"
        raise ValueError(msg)
