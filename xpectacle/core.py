from typing import Optional

import re

from . import sh
from .geometry import Geometry


def get_viewport() -> Geometry:
    '''Get current viewport geometry'''
    for line in sh.lines('wmctrl -d'):
        match = re.findall(r'.+\*.+\s+(\d+),(\d+)\s+(\d+)x(\d+)', line)

        if match:
            return Geometry(*map(int, match[0]))


def get_window() -> Geometry:
    '''Get active window bounding rectangle geometry'''
    _ = sh.output('xwininfo -all -id $(xdotool getactivewindow)')
    _ = re.findall(r'.*(?:Absolute|Width|Height).*?(\d+)', _)
    _ = map(int, _)

    return Geometry(*_)


def set_window(geometry : Geometry,
               viewport : Optional[Geometry] = None,
               window   : Optional[Geometry] = None,
               ) -> None:
    '''
    Transform active window geometry.
    `x` and `y` are relative to viewport,
    `width` and `height` are the target bounding rectangle
    '''
    # if viewport is None:
    #     viewport = get_viewport()
    # if window is None:
    #     window = get_window()

    args = ",".join(map(str, map(round, geometry)))

    sh.run(f'wmctrl -i -r $(xdotool getactivewindow) -e 0,{args}')
