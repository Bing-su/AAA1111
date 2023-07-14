from dataclasses import asdict
from typing import Any, Dict, Sized


class AsdictMixin:
    def asdict(self) -> Dict[str, Any]:
        d = asdict(self)
        for attr in self.__dataclass_fields__:
            value = getattr(self, attr)
            default = self.__dataclass_fields__[attr].default

            if value == default or (isinstance(value, Sized) and not value):
                del d[attr]
        return d
