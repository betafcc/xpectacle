import sys

from xpectacle.active_window import ActiveWindow


x, y, width, height = map(int, sys.argv[1:])

ActiveWindow().map(x=x, y=y, width=width, height=height)
