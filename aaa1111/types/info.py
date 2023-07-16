from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from beartype import beartype
from PIL import Image

from aaa1111.utils import base64_to_image

from .base import Number


@beartype
@dataclass
class PNGInfoResponse:
    info: str
    items: Dict[str, Any]


@beartype
@dataclass
class ProgressResponse:
    progress: Number
    eta_relative: Number
    state: Dict[str, Any]
    current_image: Image.Image
    textinfo: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.current_image, str):
            self.current_image = base64_to_image(self.current_image)


@beartype
@dataclass
class SamplerItem:
    name: str
    aliases: List[str]
    options: Dict[str, str]


@beartype
@dataclass
class UpscalerItem:
    name: str
    model_name: Optional[str]
    model_path: Optional[str]
    model_url: Optional[str]
    scale: Optional[Number]


@beartype
@dataclass
class LatentUpscalerModeItem:
    name: str


@beartype
@dataclass
class SDModelItem:
    title: str
    model_name: str
    hash: Optional[str]  # noqa: A003
    sha256: Optional[str]
    filename: str
    config: Optional[str]


@beartype
@dataclass
class SDVaeItem:
    model_name: str
    filename: str


@beartype
@dataclass
class HypernetworkItem:
    name: str
    path: Optional[str]


@beartype
@dataclass
class FaceRestorerItem:
    name: str
    cmd_dir: Optional[str]


@beartype
@dataclass
class RealesrganItem:
    name: str
    path: Optional[str]
    scale: Optional[int]


@beartype
@dataclass
class PromptStyleItem:
    name: str
    prompt: Optional[str]
    negative_prompt: Optional[str]


@beartype
@dataclass
class EmbeddingItem:
    step: Optional[int]
    sd_checkpoint: Optional[str]
    sd_checkpoint_name: Optional[str]
    shape: int
    vectors: int


@beartype
@dataclass
class EmbeddingsResponse:
    loaded: Dict[str, EmbeddingItem]
    skipped: Dict[str, EmbeddingItem]


@beartype
@dataclass
class MemoryResponse:
    ram: Dict[str, Any]
    cuda: Dict[str, Any]


@beartype
@dataclass
class ScriptsList:
    txt2img: List[str]
    img2img: List[str]


@beartype
@dataclass
class ScriptArg:
    label: str
    value: Optional[Any]
    minimum: Optional[Any]
    maximum: Optional[Any]
    step: Optional[Any]
    choices: Optional[List[str]]


@beartype
@dataclass
class ScriptInfo:
    name: str
    is_alwayson: bool
    is_img2img: bool
    args: List[ScriptArg]


@beartype
@dataclass
class LoraInfo:
    name: str
    alias: str
    path: str
    metadata: Dict[str, Any]


@beartype
@dataclass
class LycoInfo:
    name: str
    path: str
    metadata: Dict[str, Any]
