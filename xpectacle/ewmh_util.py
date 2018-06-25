from ewmh import EWMH
from Xlib.xobject.drawable import Window


def get_active_sub_root_window(ewmh: EWMH) -> Window:
    '''
    Get active window and climb to last parent before root
    '''

    _ = ewmh.getActiveWindow()
    root = ewmh.root

    while True:
        parent = _.query_tree().parent

        if parent == root:
            return _

        _ = parent
