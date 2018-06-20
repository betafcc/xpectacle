import sys
from time import sleep

from xpectacle.active_window import ActiveWindow


rows, columns = map(int, sys.argv[-2:])


for i in range(1, rows * columns + 1):
    ActiveWindow().tile(rows, columns, i).apply()
    sleep(0.3)
