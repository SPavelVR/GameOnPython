

from ..managers import Display
from ..node2D.collide2D import Collide2D
from ..variables import *


class NodeUI(Collide2D):

    type_name = 'NodeUI'

    def to_center_display(self):
        self.position = Vector2D(Display().get_rect().center)
        self.position.x -= self.collide.w // 2
        self.position.y -= self.collide.h // 2


    def _on_hover(self):
        self._call_signal('_on_hover')
        if self.script and hasattr(self.script, '_on_hover'): self.script._on_haver()
        pass

    def _on_mousemotion(self, motion: Vector2D):
        self._call_signal('_on_mousemotion')
        if self.script and hasattr(self.script, '_on_mousemotion'): self.script._on_mousemotion(motion)
        pass

    def _on_mouse_down(self, button: set):
        self._call_signal('_on_mouse_down')
        if self.script and hasattr(self.script, '_on_mouse_down'): self.script._on_mouse_down(button)
        pass

    def _on_mouse_pressed(self, button: set):
        self._call_signal('_on_mouse_pressed')
        if self.script and hasattr(self.script, '_on_mouse_pressed'): self.script._on_mouse_pressed(button)
        pass

    def _on_mouse_up(self, button: set):
        self._call_signal('_on_mouse_up')
        if self.script and hasattr(self.script, '_on_mouse_up'): self.script._on_mouse_up(button)
        pass

    def _on_mouse_active(self, button: set):
        self._call_signal('_on_mouse_active', button)
        pass

    pass