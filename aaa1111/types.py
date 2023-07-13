from dataclasses import asdict, dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Literal, Mapping, Optional, Sized, Union

from beartype import beartype
from PIL import Image

Number = Union[int, float]


@beartype
@dataclass
class _2IMG:  # noqa: N801
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
    script_name: Optional[str] = None
    send_images: bool = True
    save_images: bool = False
    alwayson_scripts: Mapping[str, Any] = field(default_factory=dict)

    def asdict(self) -> Dict[str, Any]:
        d = asdict(self)
        for attr in self.__dataclass_fields__:
            value = getattr(self, attr)
            default = self.__dataclass_fields__[attr].default

            if value == default or (isinstance(value, Sized) and not value):
                del d[attr]
        return d


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
    init_images: List[Union[str, Path, Image.Image]] = field(default_factory=list)
    resize_mode: Union[ResizeMode, Literal[0, 1, 2, 3]] = ResizeMode.Just_resize
    denoising_strength: Number = 0.75
    image_cfg_scale: Optional[Number] = None
    mask: Union[str, Path, Image.Image, None] = None
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


@dataclass
class Response:
    images: List[Image.Image]
    parameters: Dict[str, Any]
    info: Dict[str, Any]
