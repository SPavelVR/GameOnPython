

from pygodot import *


from .components import *
from .tileMap import TileMap
from .prograssBar import *

from .playerAttecks import *

class PlayerNode(node2D.CharacterBody2D):

    name='Player'

    MAX_HP = 10

    def __init__(self):
        super().__init__()

        self._list_animation = node2D.Node2D(parent=self)
        
        '''
        t = node2D.Text2D(filefont='./fonts/BoldPixels.ttf',
                      text='Player',
                      size=30,
                      layer=21,
                      parent=self)
        t.to_center()
        t.position.y -= 50
        '''
        
        node2D.Collision2D(layer=1,
                           mask=[1,2],
                           collide=(0,0,50,80),
                           parent=self).to_center()
        
        TileMap(parent=self)
        
        node2D.Camera2D(parent=self).to_center()

        hp = HealthComponent(parent=self,
                             MAX_HP=self.MAX_HP)

        node = ProgressBar(parent=self,
                           layer=5,
                           MAX_PROGRESS=self.MAX_HP,
                           bg_collide=(0,0,100,15),
                           bg_color=(87, 89, 82),
                           fr_color=(186, 26, 15))
        
        self._attack_list = node2D.Node2D(parent=self)
        node.set_progress(self.MAX_HP)
        node.position.y -= 50
        hp.connect('_take_damage', node.set_progress, node)
        pass

    def ready(self):

        self.animation_run: node.Node   = self.find_child('AnimationRun')
        self.animation_idle: node.Node  = self.find_child('AnimationIdle')

        self.animation_idle.play()
        self.animation_run.play()

        self.animation_run.hide()
        self.animation_idle.hide()

        self.animation_current = self.animation_idle

        self.flip_v = False
        self.speed = 750

        pass


    def process(self, delta_time):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            spw = self.find_in_tree_node('SpawnEnemies')
            spw.hide()
        elif keys[pygame.K_x]:
            spw = self.find_in_tree_node('SpawnEnemies')
            spw.show()

        player_vector = Vector2D(0,0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: 
            player_vector.x = -1
            self.flip_v = True
        if keys[pygame.K_d]: 
            player_vector.x = 1
            self.flip_v = False
        if keys[pygame.K_w]: 
            player_vector.y = -1
        if keys[pygame.K_s]: 
            player_vector.y = 1

        
        player_vector = player_vector.normilized() * self.speed * delta_time / 1000
        #player_vector = player_vector * self.speed

        self.position = self.position + player_vector

        self.position.x = round(self.position.x)
        self.position.y = round(self.position.y)

        if player_vector == Vector2D(0,0):
            if not self.animation_current is self.animation_idle:
                self.animation_current.hide()
                self.animation_current = self.animation_idle
        else:
            if not self.animation_current is self.animation_run:
                self.animation_current.hide()
                self.animation_current = self.animation_run
        
        self.animation_current.show()

        if self.flip_v != self.animation_current.flip_x:
            self.animation_current.flip_x = self.flip_v
            self.animation_current.update_shape()
        
        return super().process(delta_time)
    
    def _death_entity(self):

        dm = self.find_in_tree_node('DeathMenu')
        cn = self.find_in_tree_node('CounterDeathEnemy')

        parent = dm.parent

        for c in parent.children:
            c.hide()

        dm.show()
        cn.show()

        pass

    pass



class KnifePlayerNode(PlayerNode):

    MAX_HP = 20

    def __init__(self):
        super().__init__()

        node2D.Animation2D('Warrior_Run.png', 
                           count_repeat=0, 
                           duration=100, 
                           layer=3, 
                           sub_surface=Rect(0,0,192,192), 
                           frames=6, 
                           parent=self._list_animation, 
                           name='AnimationRun').to_center()
        
        self.anmidl = node2D.Animation2D('Warrior_Idle.png', 
                           count_repeat=0, 
                           duration=100, 
                           layer=3, 
                           sub_surface=Rect(0,0,192,192), 
                           frames=8, 
                           parent=self._list_animation, 
                           name='AnimationIdle')
        self.anmidl.to_center()
        
        self._attack_list.append_children(SwordAtteck())
        pass
    pass


class ArcherPlayerNode(PlayerNode):

    MAX_HP = 5

    def __init__(self):
        super().__init__()

        node2D.Animation2D('Archer_Run.png', 
                           count_repeat=0, 
                           duration=100, 
                           layer=3, 
                           sub_surface=Rect(0,0,192,192), 
                           frames=4, 
                           parent=self._list_animation, 
                           name='AnimationRun').to_center()
        
        self.anmidl = node2D.Animation2D('Archer_Idle.png', 
                           count_repeat=0, 
                           duration=100, 
                           layer=3, 
                           sub_surface=Rect(0,0,192,192), 
                           frames=6, 
                           parent=self._list_animation, 
                           name='AnimationIdle').to_center()
        
        self._attack_list.append_children(ArcherAtteck())
        pass
    pass