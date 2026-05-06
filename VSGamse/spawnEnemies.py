

from pygodot import *
from .enemy import EnemyNode

import random
import math


class SpawnEnemiesNode(node.Node):

    name='SpawnEnemies'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        pass

    def ready(self):

        timer = service.TimerNode(1000, parent=self)
        timer.play()

        self.enemies_node_pool = node2D.Node2D(name='EnemiesNodePool', parent=self)

        self.timer = self.find_child('TimerNode')
        self.player = self.find_in_tree_node('Player')

        self.timer.connect('repeat', self._spawn_enemy, self)

        self.enemies_pool = nodepool.NodePool(EnemyNode, 50)

        self.radius = 1500

        return super().ready()
    
    def _spawn_enemy(self):

        pos = self.player.global_position()
        
        angel = random.random() * 2 * math.pi

        vec = Vector2D(math.cos(angel), math.sin(angel)) * self.radius
        #enemy = self.enemies_pool.acquire()
        enemy = EnemyNode()
        self.enemies_node_pool.append_children(enemy)
        enemy.set_global_position(pos + vec)

        pass

    pass