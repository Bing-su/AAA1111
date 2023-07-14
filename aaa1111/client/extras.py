from abc import ABC
from pathlib import Path
from typing import Any, Mapping, Optional, Union

from beartype import beartype
from httpx import AsyncClient, Client

from aaa1111.types import (
    ExtrasBatchImages,
    ExtrasBatchImagesResponse,
    ExtrasSingleImage,
    ExtrasSingleImageResponse,
)
from aaa1111.utils import (
    aimage_to_base64,
    arecursive_read_image,
    image_to_base64,
    recursive_read_image,
)

EXTRA_SINGLE_IMAGE = "/sdapi/v1/extra-single-image"
EXTRA_BATCH_IMAGES = "/sdapi/v1/extra-batch-images"


@beartype
class ExtrasMixin(ABC):
    client: Client
    aclient: AsyncClient

    def extra_single_image(
        self,
        payload: Union[str, Path, Mapping[str, Any], ExtrasSingleImage],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        payload = self._get_payload(payload)
        if payload["image"] is not None:
            payload["image"] = image_to_base64(payload["image"])
        payload = {**payload, **kwargs}

        resp = self.client.post(
            EXTRA_SINGLE_IMAGE, json=payload, **(client_kwargs or {})
        )
        resp.raise_for_status()

        data = resp.json()
        return ExtrasSingleImageResponse(
            html_info=data["html_info"],
            image=data["image"],
        )

    async def aextra_single_image(
        self,
        payload: Union[str, Path, Mapping[str, Any], ExtrasSingleImage],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        payload = await self._aget_payload(payload)
        if payload["image"] is not None:
            payload["image"] = await aimage_to_base64(payload["image"])
        payload = {**payload, **kwargs}

        resp = await self.aclient.post(
            EXTRA_SINGLE_IMAGE, json=payload, **(client_kwargs or {})
        )
        resp.raise_for_status()

        data = resp.json()
        return ExtrasSingleImageResponse(
            html_info=data["html_info"],
            image=data["image"],
        )

    def extra_batch_images(
        self,
        payload: Union[str, Path, Mapping[str, Any], ExtrasBatchImages],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        payload = self._get_payload(payload)
        payload = recursive_read_image(payload)
        payload = {**payload, **kwargs}

        resp = self.client.post(
            EXTRA_BATCH_IMAGES, json=payload, **(client_kwargs or {})
        )
        resp.raise_for_status()

        data = resp.json()
        return ExtrasBatchImagesResponse(
            html_info=data["html_info"],
            images=data["images"],
        )

    async def aextra_batch_images(
        self,
        payload: Union[str, Path, Mapping[str, Any], ExtrasBatchImages],
        client_kwargs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ):
        payload = await self._aget_payload(payload)
        payload = await arecursive_read_image(payload)
        payload = {**payload, **kwargs}

        resp = await self.aclient.post(
            EXTRA_BATCH_IMAGES, json=payload, **(client_kwargs or {})
        )
        resp.raise_for_status()

        data = resp.json()
        return ExtrasBatchImagesResponse(
            html_info=data["html_info"],
            images=data["images"],
        )
