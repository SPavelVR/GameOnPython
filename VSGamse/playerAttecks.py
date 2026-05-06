

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
        self.enemies = self.find_in_tree_node('EnenmiesNodePool')
        return super().ready()


    pass




class SwordAtteck(node2D.Node2D):

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
            collide=Rect(0,0,500,500),
            collidable=False,
            parent=self
        )

        col.to_center()

        col.connect('on_collision', self._attack, self)

        self._damage = 10


    def _take_attack(self):
        self._can_attack = True
        self._sword_animation.hide()

    def _attack(self, collider):
        if not self._can_attack: return None

        self._sword_animation.show()
        self._sword_animation.play()
        self._can_attack = False

        hp_comp = collider.parent
        hp_comp._take_damage(self._damage)
        pass

    pass


class ArcherAtteck(node.Node):

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

    def ready(self):
        self.player = self.find_in_tree_node('Player')
        self.entity_list = self.find_in_tree_node('EnemiesNodePool')
        return super().ready()
    
    def _spaw_arrow(self):
        if not self.entity_list:
            self.entity_list = self.find_in_tree_node('EnemiesNodePool')

        if self.entity_list and len(self.entity_list.children):
            bj = self._arrow_pool.acquire()
            print('WHAT', bj, bj.visible)
            self._arrow_list.append_children(bj)
        pass

    pass


class ArrowEntity(node2D.Collide2D):


    def __init__(self, *args, **kw):

        super().__init__(*args, **kw)
        
        self.plr = None

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
        self._damage = 60
        pass

    def _attack(self, collider):
        hp_comp = collider.parent
        hp_comp._take_damage(self._damage)
        self._kill_arrow()
        pass

    def _kill_arrow(self):
        self.parent.quick_remove_child(self)

    def ready(self):
        super().ready()
        
        if self.plr is None:
            self.plr = self.find_in_tree_node('Player')

        ent = self.find_in_tree_node('EnemiesNodePool')
        ent = ent.children[random.randint(0, len(ent.children) - 1)]
        
        self.vec: Vector2D = ent.global_position() - self.plr.global_position()

        self.set_local_position(self.plr.global_position())

        self.timer.play()

        self.vec = self.vec.normilized()

        self.image.angel = self.vec.getAngel() * 180 / math.pi

        self.image.update_shape()
        pass

    def process(self, delta_time):
        
        self.set_local_position(self.local_position() + self.speed * delta_time / 1000 * self.vec)
        return super().process(delta_time)

    pass 