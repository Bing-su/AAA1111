from dataclasses import MISSING, fields
from pathlib import Path
from typing import Any, Dict, Sized, Union

from PIL import Image

ImageType = Union[str, Path, Image.Image]
PathType = Union[str, Path]
Number = Union[int, float]


class AsdictMixin:
    def asdict(self) -> Dict[str, Any]:
        d = {}
        for field in fields(self):
            value = getattr(self, field.name)
            default = field.default

            if (default is not MISSING and value != default) or (
                not isinstance(value, str) and isinstance(value, Sized) and value
            ):
                d[field.name] = value
        return d
