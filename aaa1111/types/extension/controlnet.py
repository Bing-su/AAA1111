from dataclasses import dataclass, fields
from enum import IntEnum
from typing import List, Literal, Optional, Union

from beartype import beartype

from aaa1111.types.base import ImageType, Number
from aaa1111.types.toimg import ScriptBase


class ControlNetResizeMode(IntEnum):
    RESIZE = 0
    INNER_FIT = 1
    OUTER_FIT = 2


class ControlNetControlMode(IntEnum):
    BALANCED = 0
    PROMPT = 1
    CONTROL = 2


@beartype
@dataclass
class ControlNetArgs:
    enabled: bool = True
    module: Optional[str] = None
    model: Optional[str] = None
    weight: Number = 1.0
    image: Optional[ImageType] = None
    resize_mode: Union[
        Literal[0, 1, 2], ControlNetResizeMode
    ] = ControlNetResizeMode.INNER_FIT
    low_vram: bool = False
    processor_res: int = -1
    threshold_a: Number = -1
    threshold_b: Number = -1
    guidance_start: Number = 0.0
    guidance_end: Number = 1.0
    pixel_perfect: bool = False
    control_mode: Union[
        Literal[0, 1, 2], ControlNetControlMode
    ] = ControlNetControlMode.BALANCED

    ResizeMode = ControlNetResizeMode
    ControlMode = ControlNetControlMode

    def args(self):
        d = {}
        for field in fields(self):
            value = getattr(self, field.name)
            default = field.default
            if value != default:
                d[field.name] = value
        return d


@beartype
@dataclass
class ControlNet(ScriptBase):
    _args: Union[ControlNetArgs, List[ControlNetArgs]]

    @property
    def title(self):
        return "ControlNet"

    @property
    def args(self):
        if isinstance(self._args, ControlNetArgs):
            return [self._args.args()]
        return [x.args() for x in self._args]
