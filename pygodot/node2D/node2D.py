
from ..node import Node
from ..variables import *


class Node2D(Node):

    type_name: str = "Node2D"

    position: Vector2D = Vector2D(0,0)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.position = Vector2D(kw.get("position", self.position))     
        pass
    
    def local_position(self):
        return self.position
    
    def global_position(self):
        res = self.position
        if self.parent and hasattr(self.parent, "global_position"):
            res = res + self.parent.global_position()
        return res
    
    def set_local_position(self, new_pos: Vector2D):
        self.position = new_pos
        pass

    def set_global_position(self, new_pos: Vector2D):
        pos = self.global_position() - self.local_position()
        new_pos = new_pos - pos
        self.set_local_position(new_pos)
        pass

    def process(self, delta_time):
        return super().process(delta_time)
    
    def ready(self):
        return super().ready()
    
    def finaly(self):
        return super().finaly()
    pass
