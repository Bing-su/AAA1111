from abc import ABC
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

from beartype import beartype
from httpx import AsyncClient, Client

from aaa1111.types.toimg import IMG2IMG, TXT2IMG, ScriptBase, ToImageResponse
from aaa1111.utils import (
    aload_from_file,
    arecursive_read_image,
    load_from_file,
    recursive_read_image,
)


@beartype
class ToImageMixin(ABC):
    client: Client
    aclient: AsyncClient
    defaults: Dict[str, Any]

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
        payload = self._convert_script(payload)
        payload = recursive_read_image(payload)

        resp = self.client.post(endpoint, json=payload, **(client_kwargs or {}))
        resp.raise_for_status()

        data = resp.json()
        return ToImageResponse(
            images=data["images"],
            parameters=data["parameters"],
            info=data["info"],
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
        payload = await self._aconvert_script(payload)
        payload = await arecursive_read_image(payload)

        resp = await self.aclient.post(endpoint, json=payload, **(client_kwargs or {}))
        resp.raise_for_status()
        data = resp.json()

        return ToImageResponse(
            images=data["images"],
            parameters=data["parameters"],
            info=data["info"],
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

    @staticmethod
    def _get_payload(payload: Any) -> Dict[str, Any]:
        if hasattr(payload, "asdict"):
            data = payload.asdict()
        elif is_dataclass(payload) and not isinstance(payload, type):
            data = asdict(payload)
        elif isinstance(payload, (str, Path)):
            data = load_from_file(payload)
        elif isinstance(payload, (dict, Mapping)):
            data = dict(payload)
        else:
            msg = f"Unsupported payload type: {type(payload)}"
            raise ValueError(msg)
        return data

    @staticmethod
    async def _aget_payload(payload: Any) -> Dict[str, Any]:
        if hasattr(payload, "asdict"):
            data = payload.asdict()
        elif is_dataclass(payload) and not isinstance(payload, type):
            data = asdict(payload)
        elif isinstance(payload, (str, Path)):
            data = await aload_from_file(payload)
        elif isinstance(payload, (dict, Mapping)):
            data = dict(payload)
        else:
            msg = f"Unsupported payload type: {type(payload)}"
            raise ValueError(msg)
        return data

    @staticmethod
    def _convert_script(data: Dict[str, Any]) -> Dict[str, Any]:
        for k in ("script_name", "alwayson_scripts"):
            v = data[k]
            if isinstance(v, ScriptBase):
                data[k] = v.asdict()
            elif isinstance(v, (str, Path)) and Path(v).is_file():
                data[k] = load_from_file(v)

        if isinstance(data["script_name"], Mapping):
            data["script_args"] = data["script_name"].get("args", [])
            data["script_name"] = data["script_name"]["title"]

        return data

    @staticmethod
    async def _aconvert_script(data: Dict[str, Any]) -> Dict[str, Any]:
        for k in ("script_name", "alwayson_scripts"):
            v = data[k]
            if isinstance(v, ScriptBase):
                data[k] = v.asdict()
            elif isinstance(v, (str, Path)) and Path(v).is_file():
                data[k] = await aload_from_file(v)

        if isinstance(data["script_name"], Mapping):
            data["script_args"] = data["script_name"].get("args", [])
            data["script_name"] = data["script_name"]["title"]

        return data
