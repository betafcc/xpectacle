from typing import Union
from dataclasses import dataclass, astuple


Number = Union[int, float]


@dataclass(frozen=True, order=True, eq=True)
class Geometry:
    x : Number
    y : Number
    width  : Number
    height : Number

    def __iter__(self):
        yield from astuple(self)
