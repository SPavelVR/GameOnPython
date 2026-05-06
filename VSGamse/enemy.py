
from pygodot import *

from .components import *
from .prograssBar import *

class EnemyNode(node2D.CharacterBody2D):

    name = 'Enemy'
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        anm = node2D.Animation2D('bateman.png', 
                           count_repeat=0, 
                           duration=100, 
                           layer=20, 
                           sub_surface=Rect(0,0,200,200), 
                           frames=11, 
                           parent=self, 
                           name='EnemyAnimationRun')
        anm.play()
        anm.to_center()
        
        node2D.Collision2D(layer=2,
                           mask=[1,2],
                           collide=(0,0,80,80),
                           parent=self).to_center()
        
        self.MAX_HP = 10

        hp = HealthComponent(parent=self, MAX_HP=self.MAX_HP, collision={'layer': 7})
        
        self._attack_list = node2D.Node2D(parent=self, name='ListAttack')
        AttackEnemyComponent(parent=self._attack_list)

        prg = ProgressBar(parent=self,
                           layer=5,
                           MAX_PROGRESS=self.MAX_HP,
                           bg_collide=(0,0,100,15),
                           bg_color=(87, 89, 82),
                           fr_color=(186, 26, 15))
        
        prg.set_progress(self.MAX_HP)
        prg.position.y -= 50
        hp.connect('_take_damage', prg.set_progress, prg)
        
        self.add_script(EnemyScript())
        pass

    def _death_entity(self):

        for c in self.children:
            c.hide()

        
        self.anm = node2D.Animation2D('explos.png', 
                                 Vector2D(100, 100), 
                                 layer=3, 
                                 parent=self, 
                                 count_repeat=1,
                                 frames=18,
                                 sub_surface=Rect(0,0,48,48),
                                 duration=100,
                                 name='ExitAnimation')

        self.anm.to_center()
        self.anm.play()

        self.anm.connect('timeout', self._rem_enemy, self)
        self.script = None
        pass

    def _rem_enemy(self):
        self.anm.hide()
        self.parent.quick_remove_child(self)

    pass



class EnemyScript(script.Script):


    def ready(self):

        self.player = self.owner.find_in_tree_node('Player')
        self.speed = 500

        return super().ready()
    
    def process(self, delta_time):


        self.move_enemy(delta_time)

        return super().process(delta_time)
    
    def move_enemy(self, delta_time):

        pos: Vector2D = self.owner.global_position()
        plr: Vector2D = self.player.global_position()

        scale = delta_time / 1000

        vec: Vector2D = plr - pos

        if vec.size() > (self.speed * scale):
            vec = vec.normilized() * self.speed

        vec = vec * scale

        self.owner.set_local_position(pos + vec)
        pass