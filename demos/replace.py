import sys

from xpectacle.active_window import ActiveWindow


x, y, width, height = map(int, sys.argv[1:])

ActiveWindow().move(x=x, y=y).resize(width=width, height=height).apply()