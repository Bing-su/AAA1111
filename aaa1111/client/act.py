from abc import ABC

from beartype import beartype
from httpx import AsyncClient, Client

INTERROGATE = "/sdapi/v1/interrogate"
INTERRUPT = "/sdapi/v1/interrupt"
SKIP = "/sdapi/v1/skip"
REFRESH_CHECKPOINTS = "/sdapi/v1/refresh-checkpoints"
UNLOAD_CHECKPOINT = "/sdapi/v1/unload-checkpoint"
RELOAD_CHECKPOINT = "/sdapi/v1/reload-checkpoint"
REFRESH_LORAS = "/sdapi/v1/refresh-loras"
REFRESH_LYCOS = "/sdapi/v1/refresh-lycos"


@beartype
class ActMixin(ABC):
    client: Client
    aclient: AsyncClient

    def _act(self, endpoint: str) -> None:
        resp = self.client.post(endpoint)
        resp.raise_for_status()

    async def _aact(self, endpoint: str) -> None:
        resp = await self.aclient.post(endpoint)
        resp.raise_for_status()

    def interrogate(self) -> None:
        self._act(INTERROGATE)

    async def ainterrogate(self) -> None:
        await self._aact(INTERROGATE)

    def interrupt(self) -> None:
        self._act(INTERRUPT)

    async def ainterrupt(self) -> None:
        await self._aact(INTERRUPT)

    def skip(self) -> None:
        self._act(SKIP)

    async def askip(self) -> None:
        await self._aact(SKIP)

    def refresh_checkpoints(self) -> None:
        self._act(REFRESH_CHECKPOINTS)

    async def arefresh_checkpoints(self) -> None:
        await self._aact(REFRESH_CHECKPOINTS)

    def unload_checkpoint(self) -> None:
        self._act(UNLOAD_CHECKPOINT)

    async def aunload_checkpoint(self) -> None:
        await self._aact(UNLOAD_CHECKPOINT)

    def reload_checkpoint(self) -> None:
        self._act(RELOAD_CHECKPOINT)

    async def areload_checkpoint(self) -> None:
        await self._aact(RELOAD_CHECKPOINT)

    def refresh_loras(self) -> None:
        self._act(REFRESH_LORAS)

    async def arefresh_loras(self) -> None:
        await self._aact(REFRESH_LORAS)

    def refresh_lycos(self) -> None:
        self._act(REFRESH_LYCOS)

    async def arefresh_lycos(self) -> None:
        await self._aact(REFRESH_LYCOS)
