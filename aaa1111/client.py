import asyncio
from pathlib import Path
from typing import Any, Mapping, Optional, Union

import orjson
from beartype import beartype
from httpx import AsyncClient, BasicAuth, Client

from aaa1111.types import TXT2IMG, Response
from aaa1111.utils import (
    abase64_to_image,
    aload_dict_file,
    arecursive_read_image,
    base64_to_image,
    load_dict_file,
    recursive_read_image,
)


@beartype
class AAA1111:
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
        asyncio.run(self.aclient.aclose())

    @property
    def base_url(self):
        return self.client.base_url

    @base_url.setter
    def base_url(self, url: str):
        self.client.base_url = url
        self.aclient.base_url = url

    def txt2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], TXT2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        if isinstance(payload, (str, Path)):
            payload = load_dict_file(payload)
        elif isinstance(payload, TXT2IMG):
            payload = payload.asdict()
        payload = {**self.defaults, **payload, **kwargs}
        payload = recursive_read_image(payload)

        resp = self.post("/sdapi/v1/txt2img", json=payload, **(client_kwargs or {}))
        resp.raise_for_status()
        data = resp.json()

        images = data["images"]
        images = [base64_to_image(img) for img in images]
        info = orjson.loads(data["info"])
        return Response(
            images=images,
            parameters=data["parameters"],
            info=info,
        )

    async def atxt2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], TXT2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        if isinstance(payload, (str, Path)):
            payload = await aload_dict_file(payload)
        elif isinstance(payload, TXT2IMG):
            payload = payload.asdict()
        payload = {**self.defaults, **payload, **kwargs}
        payload = await arecursive_read_image(payload)

        resp = await self.apost(
            "/sdapi/v1/txt2img", json=payload, **(client_kwargs or {})
        )
        resp.raise_for_status()
        data = resp.json()

        images = data["images"]
        images = [await abase64_to_image(img) for img in images]
        info = orjson.loads(data["info"])
        return Response(
            images=images,
            parameters=data["parameters"],
            info=info,
        )
