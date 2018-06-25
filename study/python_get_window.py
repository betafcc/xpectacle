from typing import Dict, Any, List, Callable
from types import SimpleNamespace
from dataclasses import dataclass

import Xlib
import Xlib.display

from xpectacle.geometry import Geometry


@dataclass(frozen=True)
class DisplayWrapper:
    display : Xlib.display.Display

    @classmethod
    def create(cls) -> 'DisplayWrapper':
        return cls(Xlib.display.Display())

    def find_property(self,
                      f : Callable[[str], bool],
                      ) -> Any:
        return self.get_property(next(filter(f, self.list_properties())))

    def get_root_window(self) -> Xlib.xobject.drawable.Window:
        return self.display.screen().root

    def get_all_properties(self) -> Dict[str, Any]:
        return {
            k: self.get_property(k)
            for k in self.list_properties()    
        }

    def get_property(self, name : str) -> Any:
        return self.get_root_window().get_full_property(
            self.display.intern_atom(name),
            Xlib.X.AnyPropertyType,
        )

    def list_properties(self) -> List[str]:
        return [
            self.display.get_atom_name(id)
            for id in self.get_root_window().list_properties()
        ]

    def get_work_area(self) -> Geometry:
        _ = self.get_property('_NET_CURRENT_DESKTOP')
        _ = self.get_property('_NET_WORKAREA').value[_*4:][:4]

        return Geometry(*_)

    def get_active_window(self) -> 'WindowWrapper':
        return WindowWrapper(self, self.get_active_window_resource())

    def get_active_window_resource(self) -> Xlib.xobject.drawable.Window:
        return self.display.create_resource_object('window', self.get_active_window_id())

    def get_active_window_id(self) -> int:
        return self.get_property('_NET_ACTIVE_WINDOW').value[0]


@dataclass(frozen=True)
class WindowWrapper:
    display : DisplayWrapper
    window  : Xlib.xobject.drawable.Window

    @classmethod
    def create(self) -> 'WindowWrapper':
        return DisplayWrapper.create().get_active_window()

    def find_property(self,
                      f : Callable[[str], bool],
                      ) -> Any:
        try:
            return self.get_property(next(filter(f, self.list_properties())))
        except StopIteration:
            raise ValueError('No window property name found matching condition')

    def get_sub_root_window(self) -> 'WindowWrapper':
        root    = self.display.get_root_window()
        current = self.window
        next    = current.query_tree().parent
        while next != root:
            current = next
            next    = current.query_tree().parent

        return WindowWrapper(self.display, current)

    def get_all_properties(self) -> Dict[str, Any]:
        return {
            k: self.get_property(k)
            for k in self.list_properties()    
        }

    def get_property(self, name : str) -> Any:
        return self.window.get_full_property(
            self.display.display.intern_atom(name),
            Xlib.X.AnyPropertyType,
        )

    def list_properties(self) -> List[str]:
        return [
            self.display.display.get_atom_name(id)
            for id in self.window.list_properties()
        ]

    def get_frame_extents(self) -> SimpleNamespace:
        left, right, top, bottom = self.find_property(lambda prop: 'FRAME_EXTENTS' in prop).value
        
        return SimpleNamespace(
            top=top,
            right=right,
            bottom=bottom,
            left=left,
        )

    def get_bounding_client_geometry(self) -> Geometry:
        raw_geometry = self.window.get_geometry()
        frame        = self.get_frame_extents()

        return Geometry(
            x=raw_geometry.x + frame.left,
            y=raw_geometry.y + frame.top,
            width=raw_geometry.width - (frame.left + frame.right),
            height=raw_geometry.height - (frame.top + frame.bottom),
        )


from time import sleep
from pprint import pprint


# while True:
#     pprint(
#         WindowWrapper
#         .create()
#         .get_frame_extents()
#     )
#     sleep(0.3)

# while True:
#     pprint(
#         WindowWrapper
#         .create()
#         .get_sub_root_window()
#         .window
#         .get_geometry()
#     )
#     sleep(0.3)

window   = WindowWrapper.create()
sub_root = window.get_sub_root_window()

active_geometry   = window.window.get_geometry()
sub_root_geometry = sub_root.window.get_geometry()
frame             = window.get_frame_extents()

print(SimpleNamespace(
    x=active_geometry.x - abs(frame.left),
    y=active_geometry.y - abs(frame.top),
    width=sub_root_geometry.width + (active_geometry.width - sub_root_geometry.width) - (frame.left + frame.right),
    height=sub_root_geometry.height + (active_geometry.height - sub_root_geometry.height) - (frame.top + frame.bottom),
))
