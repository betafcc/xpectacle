import sys

from xpectacle.active_window import ActiveWindow


command, *args = sys.argv[1:]

getattr(ActiveWindow(), command)(*map(int, args)).apply()
