from typing import Union

import re
from dataclasses import dataclass, astuple

from . import sh


Number = Union[int, float]


@dataclass(frozen=True, order=True, eq=True)
class Geometry:
    x : Number
    y : Number
    width  : Number
    height : Number

    def __iter__(self):
        yield from astuple(self)


def viewport() -> Geometry:
    '''Get current viewport geometry'''
    for line in sh.lines('wmctrl -d'):
        match = re.findall(r'.+\*.+\s+(\d+),(\d+)\s+(\d+)x(\d+)', line)

        if match:
            return Geometry(*map(int, match[0]))
