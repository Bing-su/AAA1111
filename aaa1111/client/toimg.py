from abc import ABC
from pathlib import Path
from typing import Any, Mapping, Optional, Union

import orjson
from beartype import beartype
from httpx import AsyncClient, Client

from aaa1111.types import IMG2IMG, TXT2IMG, ToImageResponse
from aaa1111.utils import (
    arecursive_read_image,
    recursive_read_image,
)


@beartype
class ToImageMixin(ABC):
    client: Client
    aclient: AsyncClient

    def _2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], TXT2IMG, IMG2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        *,
        endpoint: str,
        **kwargs,
    ):
        payload = self._get_payload(payload)
        payload = {**self.defaults, **payload, **kwargs}
        payload = recursive_read_image(payload)

        resp = self.client.post(endpoint, json=payload, **(client_kwargs or {}))
        resp.raise_for_status()

        data = resp.json()
        images = data["images"]
        info = orjson.loads(data["info"])
        return ToImageResponse(
            images=images,
            parameters=data["parameters"],
            info=info,
        )

    async def _a2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], TXT2IMG, IMG2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        *,
        endpoint: str,
        **kwargs,
    ):
        payload = await self._aget_payload(payload)
        payload = {**self.defaults, **payload, **kwargs}
        payload = await arecursive_read_image(payload)

        resp = await self.aclient.post(endpoint, json=payload, **(client_kwargs or {}))
        resp.raise_for_status()
        data = resp.json()

        images = data["images"]
        info = orjson.loads(data["info"])
        return ToImageResponse(
            images=images,
            parameters=data["parameters"],
            info=info,
        )

    def txt2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], TXT2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        return self._2img(
            payload,
            client_kwargs=client_kwargs,
            endpoint="/sdapi/v1/txt2img",
            **kwargs,
        )

    async def atxt2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], TXT2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        return await self._a2img(
            payload,
            client_kwargs=client_kwargs,
            endpoint="/sdapi/v1/txt2img",
            **kwargs,
        )

    def img2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], IMG2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        return self._2img(
            payload,
            client_kwargs=client_kwargs,
            endpoint="/sdapi/v1/img2img",
            **kwargs,
        )

    async def aimg2img(
        self,
        payload: Union[str, Path, Mapping[str, Any], IMG2IMG],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        return await self._a2img(
            payload,
            client_kwargs=client_kwargs,
            endpoint="/sdapi/v1/img2img",
            **kwargs,
        )
