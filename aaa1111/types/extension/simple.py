from dataclasses import dataclass

from beartype import beartype

from aaa1111.types.toimg import ScriptBase


@beartype
@dataclass
class SimpleWildcards(ScriptBase):
    @property
    def title(self):
        return "Simple wildcards"

    @property
    def args(self):
        return []
