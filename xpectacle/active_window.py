from typing import Callable, Optional
from dataclasses import dataclass, replace

from . import core
from .geometry import Geometry


@dataclass(frozen=True)
class ActiveWindow:
    transform : Callable[[Geometry, Geometry], Geometry] = lambda vp, win: win

    def apply(self) -> None:
        core.set_window(self.transform(core.get_viewport(), core.get_window()))

    def map(self,
            f : Callable[[Geometry, Geometry], Geometry],
            ) -> 'ActiveWindow':
        return replace(self, transform=lambda vp, win: self.transform(vp, f(vp, win)))

    def center(self) -> 'ActiveWindow':
        return self.center_x().center_y()

    def center_x(self) -> 'ActiveWindow':
        return self.map(lambda vp, win: replace(win, x=vp.x + (vp.width - win.width) / 2))

    def center_y(self) -> 'ActiveWindow':
        return self.map(lambda vp, win: replace(win, y=vp.y + (vp.height - win.height) / 2))

    def tile(self,
             rows        : int,
             columns     : int,
             position    : int,
             grid_width  : Optional[int] = 1,
             grid_height : Optional[int] = 1,
             ) -> 'ActiveWindow':

        def mapper(vp, win):
            width, height = vp.width / columns, vp.height / rows
            index = position - 1

            return replace(win,
                x=(index % columns) * width,
                y=(index // columns) * height,
                width=width * grid_width,
                height=height * grid_height,
            )

        return self.map(mapper)

    def corner(self,
               n : int,
               ) -> 'ActiveWindow':

        def mapper(vp, win):
            if n == 1:
                return replace(win, x=0, y=0)
            if n == 2:
                return replace(win,
                    x=vp.x + vp.width - win.width,
                    y=vp.y,
                )
            if n == 3:
                return replace(win,
                    x=vp.x,
                    y=vp.y + vp.height - win.height,
                )
            if n == 4:
                return replace(win,
                    x=vp.x + vp.width - win.width,
                    y=vp.y + vp.height - win.height,
                )

        return self.map(mapper)
