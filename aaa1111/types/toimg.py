from abc import ABC
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Literal, Mapping, Optional, Sequence, Union

import orjson
from beartype import beartype
from PIL import Image

from aaa1111.utils import base64_to_image, load_from_file

from .base import AsdictMixin, ImageType, Number


class ScriptBase(ABC):
    title: str
    args: List[Any]

    def asdict(self):
        return {self.title: {"args": self.args}}


@beartype
@dataclass
class Script(ScriptBase):
    title: str
    args: List[Any] = field(default_factory=list)


@beartype
@dataclass
class _2IMG(AsdictMixin):  # noqa: N801
    prompt: str = ""
    styles: List[str] = field(default_factory=list)
    seed: int = -1
    subseed: int = -1
    subseed_strength: Number = 0.0
    seed_resize_from_h: int = -1
    seed_resize_from_w: int = -1
    sampler_name: Optional[str] = None  # the first available sampler
    batch_size: int = 1
    n_iter: int = 1
    steps: int = 50
    cfg_scale: Number = 7.0
    width: int = 512
    height: int = 512
    restore_faces: bool = False
    tiling: bool = False
    do_not_save_samples: bool = False
    do_not_save_grid: bool = False
    negative_prompt: str = ""
    eta: Optional[Number] = None
    s_min_uncond: Number = 0.0
    s_churn: Number = 0.0
    s_tmax: Optional[Number] = None
    s_tmin: Number = 0.0
    s_noise: Number = 1.0
    override_settings: Optional[Mapping[str, Any]] = None
    override_settings_restore_afterwards: bool = True
    script_args: List[Any] = field(default_factory=list)
    script_name: Union[str, Path, ScriptBase, None] = None
    send_images: bool = True
    save_images: bool = False
    alwayson_scripts: Union[str, Path, Mapping[str, Any], Sequence[ScriptBase]] = field(
        default_factory=dict
    )

    def __post_init__(self):
        # script
        # 1. file
        if (
            isinstance(self.script_name, (str, Path))
            and Path(self.script_name).is_file()
        ):
            if self.script_args:
                msg = "if script_name is a file, script_args must be empty."
                raise ValueError(msg)
            data = load_from_file(self.script_name)
            self.script_name = data["title"]
            self.script_args = data.get("args", [])

        # 2. Script Class
        elif isinstance(self.script_name, ScriptBase):
            if self.script_args:
                msg = "if script_name is a Script object, script_args must be empty."
                raise ValueError(msg)
            self.script_args = self.script_name.args
            self.script_name = self.script_name.title

        # alwayson scripts
        # 1. file
        if isinstance(self.alwayson_scripts, (str, Path)):
            if Path(self.alwayson_scripts).is_file():
                self.alwayson_scripts = load_from_file(self.alwayson_scripts)
            else:
                msg = f"{self.alwayson_scripts!r} is not a valid file."
                raise FileNotFoundError(msg)

        # 2. Sequence of Scripts
        elif self.alwayson_scripts and isinstance(self.alwayson_scripts, Sequence):
            self.alwayson_scripts = {
                script.title: {"args": script.args} for script in self.alwayson_scripts
            }


@beartype
@dataclass
class TXT2IMG(_2IMG):
    enable_hr: bool = False
    denoising_strength: Number = 0.0
    firstphase_width: int = 0
    firstphase_height: int = 0
    hr_scale: Number = 2.0
    hr_upscaler: Optional[str] = None  # Latent (nearest)
    hr_second_pass_steps: int = 0
    hr_resize_x: int = 0
    hr_resize_y: int = 0
    hr_sampler_name: Optional[str] = None  # same as sampler_name
    hr_prompt: str = ""
    hr_negative_prompt: str = ""


class ResizeMode(IntEnum):
    Just_resize = 0
    Crop_and_resize = 1
    Resize_and_fill = 2
    Just_resize_latent_upscale = 3


class InpaintingFill(IntEnum):
    Fill = 0
    Original = 1
    Latent_noise = 2
    Latent_nothing = 3


class InpaintingMaskInvert(IntEnum):
    Inpaint_masked = 0
    Inpaint_not_masked = 1


@beartype
@dataclass
class IMG2IMG(_2IMG):
    init_images: List[ImageType] = field(default_factory=list)
    resize_mode: Union[ResizeMode, Literal[0, 1, 2, 3]] = ResizeMode.Just_resize
    denoising_strength: Number = 0.75
    image_cfg_scale: Optional[Number] = None
    mask: Optional[ImageType] = None
    mask_blur: Optional[int] = None
    mask_blur_x: int = 4
    mask_blur_y: int = 4
    inpainting_fill: Union[InpaintingFill, Literal[0, 1, 2, 3]] = InpaintingFill.Fill
    inpaint_full_res: bool = True
    inpaint_full_res_padding: int = 0
    inpainting_mask_invert: Union[
        InpaintingMaskInvert, Literal[0, 1]
    ] = InpaintingMaskInvert.Inpaint_masked
    initial_noise_multiplier: Optional[Number] = None

    ResizeMode = ResizeMode
    InpaintingFill = InpaintingFill
    InpaintingMaskInvert = InpaintingMaskInvert


@dataclass
class ToImageResponse:
    images: List[Image.Image]
    parameters: Dict[str, Any]
    info: Dict[str, Any]

    def __post_init__(self):
        if self.images and isinstance(self.images[0], str):
            self.images = [base64_to_image(img) for img in self.images]

        if isinstance(self.info, str):
            self.info = orjson.loads(self.info)
