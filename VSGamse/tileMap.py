

from pygodot import *


class TileMap(node2D.Node2D):


    name='TileMap'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        node2D.Sprite2D('TX_Tileset_Grass.png', 
                        layer=kw.get('layer', 0), 
                        collide=Rect(0,0,1600,1600),
                        sub_surface=Rect(0,0,128,128), 
                        repeat_mode=node2D.SpriteRepeatMode.REPEAT,
                        parent=self).to_center()
        
        self.add_script(TileMapeScript())
        pass
    pass


class TileMapeScript(script.Script):

    def ready(self):
        self.sprite = self.owner.find_child('Sprite2D')
        pass

    def process(self, delta_time):
        self.spriteRect: Rect = self.sprite.sub_surface
        self.spriteGlobRect: Rect = self.sprite.local_collide().copy()

        gl_pos: Vector2D = self.owner.global_position()

        res_pos: Vector2D = Vector2D(0,0)

        res_pos.x = (gl_pos.x // self.spriteRect.w) * self.spriteRect.w

        res_pos.y = (gl_pos.y // self.spriteRect.h) * self.spriteRect.h
        if gl_pos.y < 0:
            res_pos.y -= self.spriteRect.h

        self.spriteGlobRect.center = res_pos.getByTuple()
        self.sprite.set_global_position(Vector2D(self.spriteGlobRect))
        pass

    pass