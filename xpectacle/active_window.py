from typing import Callable
from dataclasses import dataclass, replace

from . import core


@dataclass(frozen=True)
class ActiveWindow:
    transform : Callable[[core.Geometry, core.Geometry], core.Geometry] = lambda vp, win: win

    def apply(self) -> None:
        core.transform(self.transform(core.viewport(), core.window()))
