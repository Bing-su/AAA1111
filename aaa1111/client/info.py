from abc import ABC
from typing import Any, Dict, List

from beartype import beartype
from httpx import AsyncClient, Client

from aaa1111.types.base import ImageType
from aaa1111.types.info import (
    EmbeddingItem,
    EmbeddingsResponse,
    FaceRestorerItem,
    HypernetworkItem,
    LatentUpscalerModeItem,
    LoraInfo,
    LycoInfo,
    MemoryResponse,
    PNGInfoResponse,
    ProgressResponse,
    PromptStyleItem,
    RealesrganItem,
    SamplerItem,
    ScriptArg,
    ScriptInfo,
    ScriptsList,
    SDModelItem,
    SDVaeItem,
    UpscalerItem,
)
from aaa1111.utils import image_to_base64

PNG_INFO = "/sdapi/v1/png-info"
PROGRESS = "/sdapi/v1/progress"
CMD_FLAGS = "/sdapi/v1/cmd-flags"
SAMPLERS = "/sdapi/v1/samplers"
UPSCALERS = "/sdapi/v1/upscalers"
LATENT_UPSCALE_MODES = "/sdapi/v1/latent-upscale-modes"
SD_MODELS = "/sdapi/v1/sd-models"
SD_VAE = "/sdapi/v1/sd-vae"
HYPERNETWORKS = "/sdapi/v1/hypernetworks"
FACE_RESTORERS = "/sdapi/v1/face-restorers"
REALESRGAN_MODELS = "/sdapi/v1/realesrgan-models"
PROMPT_STYLES = "/sdapi/v1/prompt-styles"
EMBEDDINGS = "/sdapi/v1/embeddings"
MEMORY = "/sdapi/v1/memory"
SCRIPTS = "/sdapi/v1/scripts"
SCRIPT_INFO = "/sdapi/v1/script-info"
LORAS = "/sdapi/v1/loras"
LYCOS = "/sdapi/v1/lycos"


@beartype
class InfoMixin(ABC):
    client: Client
    aclient: AsyncClient

    def png_info(self, image: ImageType):
        image = image_to_base64(image)
        resp = self.client.post(PNG_INFO, json={"image": image})
        resp.raise_for_status()
        return PNGInfoResponse(**resp.json())

    async def apng_info(self, image: ImageType):
        image = image_to_base64(image)
        resp = await self.aclient.post(PNG_INFO, json={"image": image})
        resp.raise_for_status()
        return PNGInfoResponse(**resp.json())

    def progress(self, skip_current_image: bool = False):
        resp = self.client.get(
            PROGRESS, params={"skip_current_image": skip_current_image}
        )
        resp.raise_for_status()
        return ProgressResponse(**resp.json())

    async def aprogress(self, skip_current_image: bool = False):
        resp = await self.aclient.get(
            PROGRESS, params={"skip_current_image": skip_current_image}
        )
        resp.raise_for_status()
        return ProgressResponse(**resp.json())

    def cmd_flags(self) -> Dict[str, Any]:
        resp = self.client.get(CMD_FLAGS)
        resp.raise_for_status()
        return resp.json()

    async def acmd_flags(self) -> Dict[str, Any]:
        resp = await self.aclient.get(CMD_FLAGS)
        resp.raise_for_status()
        return resp.json()

    def samplers(self) -> List[SamplerItem]:
        resp = self.client.get(SAMPLERS)
        resp.raise_for_status()
        return [SamplerItem(**item) for item in resp.json()]

    async def asamplers(self) -> List[SamplerItem]:
        resp = await self.aclient.get(SAMPLERS)
        resp.raise_for_status()
        return [SamplerItem(**item) for item in resp.json()]

    def upscalers(self) -> List[UpscalerItem]:
        resp = self.client.get(UPSCALERS)
        resp.raise_for_status()
        return [UpscalerItem(**item) for item in resp.json()]

    async def aupscalers(self) -> List[UpscalerItem]:
        resp = await self.aclient.get(UPSCALERS)
        resp.raise_for_status()
        return [UpscalerItem(**item) for item in resp.json()]

    def latent_upscale_modes(self) -> List[LatentUpscalerModeItem]:
        resp = self.client.get(LATENT_UPSCALE_MODES)
        resp.raise_for_status()
        return [LatentUpscalerModeItem(**item) for item in resp.json()]

    async def alatent_upscale_modes(self) -> List[LatentUpscalerModeItem]:
        resp = await self.aclient.get(LATENT_UPSCALE_MODES)
        resp.raise_for_status()
        return [LatentUpscalerModeItem(**item) for item in resp.json()]

    def sd_models(self) -> List[SDModelItem]:
        resp = self.client.get(SD_MODELS)
        resp.raise_for_status()
        return [SDModelItem(**item) for item in resp.json()]

    async def asd_models(self) -> List[SDModelItem]:
        resp = await self.aclient.get(SD_MODELS)
        resp.raise_for_status()
        return [SDModelItem(**item) for item in resp.json()]

    def sd_vae(self) -> List[SDVaeItem]:
        resp = self.client.get(SD_VAE)
        resp.raise_for_status()
        return [SDVaeItem(**item) for item in resp.json()]

    async def asd_vae(self) -> List[SDVaeItem]:
        resp = await self.aclient.get(SD_VAE)
        resp.raise_for_status()
        return [SDVaeItem(**item) for item in resp.json()]

    def hypernetworks(self) -> List[HypernetworkItem]:
        resp = self.client.get(HYPERNETWORKS)
        resp.raise_for_status()
        return [HypernetworkItem(**item) for item in resp.json()]

    async def ahypernetworks(self) -> List[HypernetworkItem]:
        resp = await self.aclient.get(HYPERNETWORKS)
        resp.raise_for_status()
        return [HypernetworkItem(**item) for item in resp.json()]

    def face_restorers(self) -> List[FaceRestorerItem]:
        resp = self.client.get(FACE_RESTORERS)
        resp.raise_for_status()
        return [FaceRestorerItem(**item) for item in resp.json()]

    async def aface_restorers(self) -> List[FaceRestorerItem]:
        resp = await self.aclient.get(FACE_RESTORERS)
        resp.raise_for_status()
        return [FaceRestorerItem(**item) for item in resp.json()]

    def realesrgan_models(self) -> List[RealesrganItem]:
        resp = self.client.get(REALESRGAN_MODELS)
        resp.raise_for_status()
        return [RealesrganItem(**item) for item in resp.json()]

    async def arealesrgan_models(self) -> List[RealesrganItem]:
        resp = await self.aclient.get(REALESRGAN_MODELS)
        resp.raise_for_status()
        return [RealesrganItem(**item) for item in resp.json()]

    def prompt_styles(self) -> List[PromptStyleItem]:
        resp = self.client.get(PROMPT_STYLES)
        resp.raise_for_status()
        return [PromptStyleItem(**item) for item in resp.json()]

    async def aprompt_styles(self) -> List[PromptStyleItem]:
        resp = await self.aclient.get(PROMPT_STYLES)
        resp.raise_for_status()
        return [PromptStyleItem(**item) for item in resp.json()]

    def embeddings(self) -> EmbeddingsResponse:
        resp = self.client.get(EMBEDDINGS)
        resp.raise_for_status()
        data = resp.json()
        loaded = {k: EmbeddingItem(**v) for k, v in data["loaded"].items()}
        skipped = {k: EmbeddingItem(**v) for k, v in data["skipped"].items()}
        return EmbeddingsResponse(loaded=loaded, skipped=skipped)

    async def aembeddings(self) -> EmbeddingsResponse:
        resp = await self.aclient.get(EMBEDDINGS)
        resp.raise_for_status()
        data = resp.json()
        loaded = {k: EmbeddingItem(**v) for k, v in data["loaded"].items()}
        skipped = {k: EmbeddingItem(**v) for k, v in data["skipped"].items()}
        return EmbeddingsResponse(loaded=loaded, skipped=skipped)

    def memory(self) -> MemoryResponse:
        resp = self.client.get(MEMORY)
        resp.raise_for_status()
        return MemoryResponse(**resp.json())

    async def amemory(self) -> MemoryResponse:
        resp = await self.aclient.get(MEMORY)
        resp.raise_for_status()
        return MemoryResponse(**resp.json())

    def scripts(self) -> ScriptsList:
        resp = self.client.get(SCRIPTS)
        resp.raise_for_status()
        return ScriptsList(**resp.json())

    async def ascripts(self) -> ScriptsList:
        resp = await self.aclient.get(SCRIPTS)
        resp.raise_for_status()
        return ScriptsList(**resp.json())

    def script_info(self) -> List[ScriptInfo]:
        resp = self.client.get(SCRIPT_INFO)
        resp.raise_for_status()
        return [
            ScriptInfo(
                name=item["name"],
                is_alwayson=item["is_alwayson"],
                is_img2img=item["is_img2img"],
                args=[ScriptArg(**arg) for arg in item["args"]],
            )
            for item in resp.json()
        ]

    async def ascript_info(self) -> List[ScriptInfo]:
        resp = await self.aclient.get(SCRIPT_INFO)
        resp.raise_for_status()
        return [
            ScriptInfo(
                name=item["name"],
                is_alwayson=item["is_alwayson"],
                is_img2img=item["is_img2img"],
                args=[ScriptArg(**arg) for arg in item["args"]],
            )
            for item in resp.json()
        ]

    def loras(self) -> List[LoraInfo]:
        resp = self.client.get(LORAS)
        resp.raise_for_status()
        return [LoraInfo(**item) for item in resp.json()]

    async def aloras(self) -> List[LoraInfo]:
        resp = await self.aclient.get(LORAS)
        resp.raise_for_status()
        return [LoraInfo(**item) for item in resp.json()]

    def lycos(self) -> List[LycoInfo]:
        resp = self.client.get(LYCOS)
        resp.raise_for_status()
        return [LycoInfo(**item) for item in resp.json()]

    async def alycos(self) -> List[LycoInfo]:
        resp = await self.aclient.get(LYCOS)
        resp.raise_for_status()
        return [LycoInfo(**item) for item in resp.json()]
