from typing import Union

from dataclasses import dataclass, astuple, replace


Number = Union[int, float]


@dataclass(frozen=True, order=True, eq=True)
class Geometry:
    x : Number
    y : Number
    width  : Number
    height : Number

    def __iter__(self):
        yield from astuple(self)


    def align_to(self,
                 reference : 'Geometry',
                 ) -> 'Geometry':
        '''Sums origin to reference origin'''

        return replace(self,
            x=self.x + reference.x,
            y=self.y + reference.y,
        )
