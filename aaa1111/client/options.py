from abc import ABC
from typing import Any, Dict

from beartype import beartype
from httpx import AsyncClient, Client

OPTIONS = "/sdapi/v1/options"


@beartype
class OptionsMixin(ABC):
    client: Client
    aclient: AsyncClient

    def get_options(self) -> Dict[str, Any]:
        resp = self.client.get(OPTIONS)
        resp.raise_for_status()
        return resp.json()

    async def aget_options(self) -> Dict[str, Any]:
        resp = await self.aclient.get(OPTIONS)
        resp.raise_for_status()
        return resp.json()

    def set_options(self, **kwargs: Any) -> None:
        resp = self.client.post(OPTIONS, json=kwargs)
        resp.raise_for_status()

    async def aset_options(self, **kwargs: Any) -> None:
        resp = await self.aclient.post(OPTIONS, json=kwargs)
        resp.raise_for_status()
