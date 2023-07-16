from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import List, Literal, Optional, Union

from beartype import beartype
from PIL import Image

from aaa1111.utils import base64_to_image

from .base import AsdictMixin, ImageType, Number, PathType


class ResizeMode(IntEnum):
    Scale_by = 0
    Scale_to = 1


@beartype
@dataclass
class ExtraBase(AsdictMixin):
    resize_mode: Union[ResizeMode, Literal[0, 1]] = ResizeMode.Scale_by
    show_extras_results: bool = True
    gfpgan_visibility: Number = 0.0
    codeformer_visibility: Number = 0.0
    codeformer_weight: Number = 0.0
    upscaling_resize: Number = 2.0
    upscaling_resize_w: int = 512
    upscaling_resize_h: int = 512
    upscaling_crop: bool = True
    upscaler_1: str = "None"
    upscaler_2: str = "None"
    extras_upscaler_2_visibility: Number = 0.0
    upscale_first: bool = False

    ResizeMode = ResizeMode


@beartype
@dataclass
class ExtrasSingleImage(ExtraBase):
    image: Optional[ImageType] = None


@beartype
@dataclass
class FileData:
    data: ImageType
    name: str = ""  # never used (v1.4.1)

    def __post_init__(self):
        if not self.name and isinstance(self.data, PathType):
            self.name = Path(self.data).name


@beartype
@dataclass
class ExtrasBatchImages(ExtraBase):
    imageList: List[FileData] = field(default_factory=list)  # noqa: N815


@dataclass
class ExtrasSingleImageResponse:
    html_info: str
    image: Image.Image

    def __post_init__(self):
        if isinstance(self.image, str):
            self.image = base64_to_image(self.image)


@dataclass
class ExtrasBatchImagesResponse:
    html_info: str
    images: List[Image.Image]

    def __post_init__(self):
        if self.images and isinstance(self.images[0], str):
            self.images = [base64_to_image(img) for img in self.images]
