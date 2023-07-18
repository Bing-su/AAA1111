from dataclasses import dataclass, fields
from enum import Enum
from typing import Union

from beartype import beartype

from aaa1111.types.base import Number
from aaa1111.types.toimg import ScriptBase

VALID_MODES = [
    "Constant",
    "Linear Down",
    "Cosine Down",
    "Half Cosine Down",
    "Linear Up",
    "Cosine Up",
    "Half Cosine Up",
    "Power Up",
    "Power Down",
    "Linear Repeating",
    "Cosine Repeating",
    "Sawtooth",
]


class MODES(Enum):
    Constant = "Constant"
    Linear_Down = "Linear Down"
    Cosine_Down = "Cosine Down"
    Half_Cosine_Down = "Half Cosine Down"
    Linear_Up = "Linear Up"
    Cosine_Up = "Cosine Up"
    Half_Cosine_Up = "Half Cosine Up"
    Power_Up = "Power Up"
    Power_Down = "Power Down"
    Linear_Repeating = "Linear Repeating"
    Cosine_Repeating = "Cosine Repeating"
    Sawtooth = "Sawtooth"


@beartype
@dataclass
class DynamicThresholding(ScriptBase):
    enabled: bool = True  # original is `False`
    mimic_scale: Number = 7.0
    threshold_percentile: Number = 100.0
    mimic_mode: Union[str, MODES] = MODES.Constant
    mimic_scale_min: Number = 0.0
    cfg_mode: Union[str, MODES] = MODES.Constant
    cfg_scale_min: Number = 0.0
    sched_val: Number = 4.0

    MODES = MODES

    @property
    def title(self):
        return "Dynamic Thresholding (CFG Scale Fix)"

    @property
    def args(self):
        a = [getattr(self, field.name) for field in fields(self)]
        return [x.value if isinstance(x, Enum) else x for x in a]
