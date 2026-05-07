


from .collide2D import *
from ..variables import *
from ..systems import CollisionSystem



class Collision2D(Collide2D):

    type_name: str = "Collision2D"

    include_systems = [CollisionSystem]

    layer: int = 0
    mask: int = None

    collidable = True
    heavy = 0

    def __init__(self, *args, **kw):
        self.layer = 1 << clamp(kw.get("layer", 0), 0, 32)
        self.mask  = getMaskByList(map(lambda x: clamp(x, 0, 32), kw.get('mask', [])))

        self.collidable = kw.get('collidable', self.collidable)
        super().__init__(*args, **kw)
        pass


    def on_collision(self, collision_node):
        
        self._call_signal("on_collision", collision_node)
        if self.script and hasattr(self.script, 'on_collision'): self.script.on_collision(collision_node)
        pass
    
    def find_character_body(self):

        parent = self.parent

        while (not parent and parent.type_name != 'CharacterBody2D'):
            parent = parent.parent

        return parent
    pass