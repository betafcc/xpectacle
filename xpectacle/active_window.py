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
