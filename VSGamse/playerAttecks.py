

from pygodot import *

import math
import random
from .components import *

class BaseAttack(node2D.Node2D):


    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        pass

    def ready(self):

        self.player = self.find_in_tree_node('Player')
        self.enemies = self.find_in_tree_node('EnemiesNodePool')
        return super().ready()


    pass




class SwordAtteck(BaseAttack):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self._can_attack = True

        self._sword_animation = MultiFileAnimation(parent=self,
                                                   duration=200,
                                                   images=[f'./assets/blue_sword/File{i}.png' for i in range(1, 7)],
                                                   layer=3,
                                                   count_repeat=1)
        
        self._sword_animation.to_center()
        self._sword_animation.connect('timeout', self._take_attack, self)
        self._sword_animation.hide()

        
        col = node2D.Collision2D(
            layer=6,
            mask=[7],
            collide=Rect(0,0,800,800),
            collidable=False,
            parent=self
        )

        col.to_center()

        col.connect('on_collision', self._attack, self)

        self._damage = 10
        self.state = True


    def _take_attack(self):
        self._can_attack = True
        self._sword_animation.hide()

    def _attack(self, collider):
        if not self._can_attack: return None

        if self.state:
            self._sword_animation.show()
            self._sword_animation.play()
            self.state = False

        hp_comp = collider.parent
        hp_comp._take_damage(self._damage)
        pass

    def process(self, delta_time):
        if not self.state:
            self.state = True
            self._can_attack = False

        if self.player.flip_v != self._sword_animation.flip_x:
            self._sword_animation.flip_x = self.player.flip_v
            self._sword_animation.update_shape()

        return super().process(delta_time)

    pass


class ArcherAtteck(BaseAttack):

    name='ArcherAttack'

    _arrow_pool = None

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._arrow_list = node.Node(parent=self)

        self.timer = service.TimerNode(500,
                                       0,
                                       parent=self)
    

        self.timer.connect('repeat', self._spaw_arrow, self)

        self._arrow_pool = nodepool.NodePool(ArrowEntity)
        
        pass
    
    def _spaw_arrow(self):
        if not self.enemies:
            self.enemies = self.find_in_tree_node('EnemiesNodePool')

        if self.enemies and len(self.enemies.children):
            bj = self._arrow_pool.acquire()
            self._arrow_list.append_children(bj)
        pass

    pass


class ArrowEntity(BaseAttack):


    def __init__(self, *args, **kw):

        super().__init__(*args, **kw)
        
        self.player = None

        self.image = node2D.Sprite2D(parent=self,
                                     image_name='Arrow.png',
                                     layer = 30,
                                     scale=Vector2D(90,90),
                                     )
        
        self.timer = service.TimerNode(3000,
                                       1,
                                       parent=self)
        
        col = node2D.Collision2D(
            layer=6,
            mask=[7],
            collide=Rect(0,0,50,50),
            collidable=False
        )

        col.to_center()

        col.connect('on_collision', self._attack, self)

        self.append_children(col)

        self.col = col

        self.timer.connect('timeout', self._kill_arrow, self)

        self.speed = 300
        self._damage = 5
        pass

    def _attack(self, collider):
        hp_comp = collider.parent
        hp_comp._take_damage(self._damage)
        self._kill_arrow()
        pass

    def _kill_arrow(self):
        if self.parent:
            self.parent.quick_remove_child(self)

    def ready(self):
        super().ready()

        ent = self.enemies.children[random.randint(0, len(self.enemies.children) - 1)]
        
        self.vec: Vector2D = ent.global_position() - self.player.global_position()

        self.set_local_position(self.player.global_position() - Vector2D(self.image.local_collide().center))



        self.timer.play()

        self.vec = self.vec.normilized()

        self.image.angel = self.vec.getAngel() * 180 / math.pi

        self.image.update_shape()
        pass

    def process(self, delta_time):
        
        self.set_local_position(self.local_position() + self.speed * delta_time / 1000 * self.vec)
        return super().process(delta_time)

    pass 