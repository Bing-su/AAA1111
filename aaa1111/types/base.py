from dataclasses import asdict, fields
from pathlib import Path
from typing import Any, Dict, Sized, Union

from PIL import Image

ImageType = Union[str, Path, Image.Image]
PathType = Union[str, Path]
Number = Union[int, float]


class AsdictMixin:
    def asdict(self) -> Dict[str, Any]:
        d = asdict(self)
        for field in fields(self):
            value = getattr(self, field.name)
            default = field.default

            if value == default or (isinstance(value, Sized) and not value):
                d.pop(field.name, None)
        return d
