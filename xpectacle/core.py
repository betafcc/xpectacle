from typing import Optional

import re

from ewmh import EWMH

from . import sh
from .geometry import Geometry


ewmh = EWMH()


def get_workarea() -> Geometry:
    '''Get current workarea geometry'''
    _ = ewmh.getCurrentDesktop()
    _ = ewmh.getWorkArea()[_*4:][:4]
    _ = Geometry(*_)

    return _


def get_window() -> Geometry:
    '''Get active window bounding rectangle geometry'''
    _ = sh.output('xwininfo -all -id $(xdotool getactivewindow)')
    _ = re.findall(r'.*(?:Absolute|Width|Height).*?(\d+)', _)
    _ = map(int, _)

    return Geometry(*_)


def set_window(geometry : Geometry,
               workarea : Optional[Geometry] = None,
               window   : Optional[Geometry] = None,
               ) -> None:
    '''
    Transform active window geometry.
    `x` and `y` are relative to workarea,
    `width` and `height` are the target bounding rectangle
    '''
    if workarea is None:
        workarea = get_workarea()
    if window is None:
        window = get_window()

    _ = geometry.align_to(workarea)
    _ = ",".join(map(str, map(round, _)))

    sh.run(f'wmctrl -i -r $(xdotool getactivewindow) -e 0,{_}')
