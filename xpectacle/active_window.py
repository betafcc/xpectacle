from typing import Callable
from dataclasses import dataclass, replace

from . import core


@dataclass(frozen=True)
class ActiveWindow:
    transform : Callable[[core.Geometry, core.Geometry], core.Geometry] = lambda vp, win: win

    def apply(self) -> None:
        core.transform(self.transform(core.viewport(), core.window()))

    def map(self,
            f : Callable[[core.Geometry, core.Geometry], core.Geometry],
            ) -> 'ActiveWindow':
        return replace(self, transform=lambda vp, win: self.transform(vp, f(vp, win)))

    def center(self) -> 'ActiveWindow':
        return self.center_x().center_y()

    def center_x(self) -> 'ActiveWindow':
        return self.map(lambda vp, win: replace(win, x=vp.x + (vp.width - win.width) / 2))

    def center_y(self) -> 'ActiveWindow':
        return self.map(lambda vp, win: replace(win, y=vp.y + (vp.height - win.height) / 2))

    def tile(self,
             rows     : int,
             columns  : int,
             position : int,
             ) -> 'ActiveWindow':

        def mapper(vp, win):
            width, height = vp.width / columns, vp.height / rows
            index = position - 1

            return replace(win,
                x=(index % columns) * width,
                y=(index // columns) * height,
                width=width,
                height=height,
            )

        return self.map(mapper)
