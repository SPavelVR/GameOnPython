


from .node2D import *
from ..variables import *

class Collide2D(Node2D):

    type_name: str = "Collide2D"

    collide: Rect = Rect(0,0,0,0)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.collide = Rect(kw.get("collide", self.collide))
        pass
    
    def local_collide(self):
        return (self.collide + self.position)
    
    def global_collide(self):
        vec = self.global_position()
        return (vec + self.collide)
    
    def to_center(self):
        self.position = Vector2D(-self.collide.centerx, -self.collide.centery)
    pass