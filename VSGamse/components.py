
from pygodot import *



class HealthComponent(node2D.Node2D):

    name = 'HealthComponent'
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        col = node2D.Collision2D(
            **kw.get('collision', {'layer': 5, 'mask': []}),
            collide=Rect(0,0,100,100),
            collidable = False,
            parent=self
        )
        col.to_center()

        self._take_damage_timer = service.TimerNode(500, 1, parent=self)

        self._take_damage_timer.connect('timeout', self._enable_taking_damage, self)

        self._can_take_damage = True
        self.MAX_HP = kw.get('MAX_HP', 10)
        pass
    
    def _take_damage(self, damage: int):

        if not self._can_take_damage: return

        #self._can_take_damage = False
        #self._take_damage_timer.play()

        
        self.current_HP = clamp(self.current_HP - damage, 0, self.MAX_HP)

        self._call_signal('_take_damage', self.current_HP)

        if self.current_HP == 0 and hasattr(self.parent, '_death_entity'):
            self._call_signal('_death_hp')
            self.parent._death_entity()

        print(f'Detected -Heal <<{damage}>> hp is {self.current_HP}')
        pass

    def _enable_taking_damage(self):
        self._can_take_damage = True
        pass
    
    def ready(self):
        self.current_HP = self.MAX_HP

        return super().ready()
    
    def process(self, delta_time):
        return super().process(delta_time)
    
    def finaly(self):
        return super().finaly()
    
    pass


class AttackEnemyComponent(node2D.Node2D):

    name = 'AttackEntityComponent'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        col = node2D.Collision2D(
            layer=8,
            mask=[5],
            collide=Rect(0,0,200,200),
            collidable=False,
            parent=self
        )

        col.to_center()

        col.connect('on_collision', self._attack, self)

        self._sword_attck = MultiFileAnimation(parent=self,
                                               images=[f'./assets/red_sword/File{i}.png' for i in range(1, 7)],
                                               layer=3,
                                               count_repeat=1)
        self._sword_attck.to_center()

        self._sword_attck.connect('timeout', self._take_attack, self)

        self._can_attack = True

        self._damage = 1
        pass

    def _take_attack(self):
        self._can_attack = True
        self._sword_attck.hide()

    def _attack(self, player_collide):

        if not self._can_attack: return None

        self._sword_attck.show()
        self._sword_attck.play()
        self._can_attack = False

        hp_comp = player_collide.parent
        hp_comp._take_damage(self._damage)
        pass

    def ready(self):
        return super().ready()
    
    def process(self, delta_time):
        if self._can_attack: self._sword_attck.visible = False
        return super().process(delta_time)
    
    def finaly(self):
        return super().finaly()

    pass



class MultiFileAnimation(node2D.Sprite2D):


    def __init__(self, image_name = '', scale=Vector2D(0,0), sub_surface=Rect(0,0,0,0), repeat_mode=node2D.SpriteRepeatMode.CLAMP, *args, **kw):
        super().__init__(image_name, scale, sub_surface, repeat_mode, *args, **kw)


        self.images = [managers.ManagerImage().load(i) for i in kw.get('images', [])]
        self.count_images = len(self.images)
        self.current_image = self.images[0]

        count_repeat = kw.get('count_repeat', 0) * self.count_images
        if count_repeat: count_repeat -= 1
        self.timer = service.TimerNode(kw.get('duration', 200), count_repeat, running=False, parent=self)
        
        self.timer.connect('repeat', self.update_animation, self)
        self.timer.connect('timeout', self.time_out_animation, self)

        self.time_out_animation()
        pass


    def update_animation(self):
        self.current_image = (self.current_image + 1) % self.count_images
        self.image = self.images[self.current_image]
        self.place_image()
        pass

    def time_out_animation(self):
        self.current_image = 0
        self.image = self.images[0]
        self.place_image()
        self._call_signal('timeout')
        pass

    def play(self):
        self.timer.play()
    pass
