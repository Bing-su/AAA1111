from dataclasses import asdict, fields
from typing import Any, Dict, Sized


class AsdictMixin:
    def asdict(self) -> Dict[str, Any]:
        d = asdict(self)
        for field in fields(self):
            value = getattr(self, field.name)
            default = field.default

            if value == default or (isinstance(value, Sized) and not value):
                d.pop(field.name, None)
        return d
