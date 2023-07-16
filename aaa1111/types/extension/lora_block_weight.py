from dataclasses import dataclass, fields
from enum import Enum, IntEnum
from typing import Literal, Union

from beartype import beartype

from aaa1111.types.toimg import ScriptBase

_lbw_loraratios_default = "\
NONE:0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n\
ALL:1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\n\
INS:1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0\n\
IND:1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0\n\
INALL:1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0\n\
MIDD:1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0\n\
OUTD:1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0\n\
OUTS:1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1\n\
OUTALL:1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1\n\
ALL0.5:0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"


_elemental_default = "\
ATTNDEEPON:IN05-OUT05:attn:1\n\n\
ATTNDEEPOFF:IN05-OUT05:attn:0\n\n\
PROJDEEPOFF:IN05-OUT05:proj:0\n\n\
XYZ:::1"


class XYZSetting(IntEnum):
    Disable = 0
    XYZ_plot = 1
    Effective_Block_Analyzer = 2


class ATYPES(Enum):
    none = "none"
    Block_ID = "Block ID"
    values = "values"
    seed = "seed"
    Original_Weights = "Original Weights"
    elements = "elements"


class Diffcol(Enum):
    black = "black"
    white = "white"


@beartype
@dataclass
class LoRABlockWeight(ScriptBase):
    lbw_loraratios: str = _lbw_loraratios_default
    lbw_useblocks: bool = True
    xyzsetting: Union[Literal[0, 1, 2], XYZSetting] = XYZSetting.Disable
    xtype: Union[str, ATYPES] = ATYPES.values
    xmen: str = "0,0.25,0.5,0.75,1"
    ytype: Union[str, ATYPES] = ATYPES.Block_ID
    ymen: str = "IN05-OUT05"
    ztype: Union[str, ATYPES] = ATYPES.none
    zmen: str = ""
    exmen: str = "0.5,1"
    eymen: str = "BASE,IN00,IN01,IN02,IN03,IN04,IN05,IN06,IN07,IN08,IN09,IN10,IN11,M00,OUT00,OUT01,OUT02,OUT03,OUT04,OUT05,OUT06,OUT07,OUT08,OUT09,OUT10,OUT11"
    ecount: int = 1
    diffcol: Union[str, Diffcol] = Diffcol.black
    thresh: Union[int, str] = 20  # original is str, but only used as integer
    revxy: bool = False
    elemental: str = _elemental_default
    elemsets: bool = False

    XYZSetting = XYZSetting
    ATYPES = ATYPES
    Diffcol = Diffcol

    @property
    def title(self):
        return "LoRA Block Weight"

    @property
    def args(self):
        a = [getattr(self, field.name) for field in fields(self)]
        return [x.value if isinstance(x, Enum) else x for x in a]
