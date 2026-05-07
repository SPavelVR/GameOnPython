

from pygodot import *
from .player import *
from .createGame import *

class MainSelectionMenu(nodeUI.NodeUI):


    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        display_rect = managers.Display().get_rect()

        self.bg = nodeUI.ShapeUI(parent=self,
                                 color=(84, 83, 81),
                                 layer=0,
                                 collide=display_rect)
        

        
        self.selButArcher = SelectionArea(parent=self,
                                           color=(143, 141, 137),
                                           layer=1,
                                           collide=Rect(0,0,100,60),
                                           color_on_hover=(255, 141, 137),
                                           color_on_mouse_down=(255,255,255),
                                           position=(display_rect.w // 2 - 300, display_rect.h // 2 - 80))
        
        txt = nodeUI.TextUI(parent=self.selButArcher,
                      color=(0,0,0),
                      layer=2,
                      size=30,
                      text='Archer',
                      filefont='./fonts/BoldPixels.ttf'
                      )
        
        txt.position = Vector2D((self.selButArcher.collide.w - txt.collide.w) // 2 , (self.selButArcher.collide.h - txt.collide.h) // 2)


        self.selButKnight = SelectionArea(parent=self,
                                           color=(143, 141, 137),
                                           layer=1,
                                           collide=Rect(0,0,100,60),
                                           color_on_hover=(255, 141, 137),
                                           color_on_mouse_down=(255,255,255),
                                           position=(display_rect.w // 2 + 200, display_rect.h // 2 - 80))
        
        txt = nodeUI.TextUI(parent=self.selButKnight,
                      color=(0,0,0),
                      layer=2,
                      size=30,
                      text='Knife',
                      filefont='./fonts/BoldPixels.ttf'
                      )
        
        txt.position = Vector2D((self.selButArcher.collide.w - txt.collide.w) // 2 , (self.selButArcher.collide.h - txt.collide.h) // 2)
        
        self.selButArcher.connect('_on_mouse_active', self._selection_archor, self)
        self.selButKnight.connect('_on_mouse_active', self._selection_knife, self)

        self._selection_player = None
        pass
        

    def _selection_archor(self, button):

        if not (1 in button): return None

        self._selection_player = ArcherPlayerNode()

        self._start_game()
        pass

    def _selection_knife(self, button):

        if not (1 in button): return None

        self._selection_player = KnifePlayerNode()

        self._start_game()
        pass

    def _start_game(self):
        
        game = self.find_in_tree_node('Game')
        game.show()
        game.append_children(self._selection_player)
        
        CreateGame(game)

        self.hide()

        print(f'Start game with <<{self._selection_player}>>')
        pass

    pass


class SelectionArea(nodeUI.ShapeUI):


    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self._color_on_hover = Vector3D(kw.get('color_on_hover', self.color))
        self._color_on_mouse_down = Vector3D(kw.get('color_on_mouse_down', self._color_on_hover))

        self.base_color = self.color
        self._flag_on_hover = False
        self._flag_on_mouse_down = False
        pass

    def _on_hover(self):
        if not self._flag_on_hover and not self._flag_on_mouse_down :
            self.color = self._color_on_hover
            self._flag_on_hover = True
            self.update_shape()
        return super()._on_hover()
    
    def _on_mouse_active(self, button):

        if (1 in button) and not self._flag_on_mouse_down:
            self.color = self._color_on_mouse_down
            self._flag_on_mouse_down = True
            self.update_shape()
        super()._on_mouse_active(button)
        pass

    def process(self, delta_time):

        if not (self._flag_on_hover or self._flag_on_mouse_down):
            self.color = self.base_color
            self.update_shape()


        self._flag_on_hover = False
        self._flag_on_mouse_down = False
        return super().process(delta_time)

    pass



from pygodot import *

class DeathMenu(nodeUI.NodeUI):
    
    name = 'DeathMenu'
    
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        
        display_rect = managers.Display().get_rect()
        
        self.bg = nodeUI.ShapeUI(
            parent=self,
            color=(180, 30, 30), 
            layer=0,
            collide=display_rect
        )
        
        self.title_text = nodeUI.TextUI(
            parent=self,
            color=(255, 255, 255),
            layer=1,
            size=60,
            text='ВЫ ПРОИГРАЛИ',
            filefont='./fonts/BoldPixels.ttf'
        )
        
        text_rect = self.title_text.collide
        self.title_text.position = Vector2D(
            (display_rect.w - text_rect.w) // 2,
            display_rect.h // 2 - 100
        )
        
        self.exit_button = SelectionArea(
            parent=self,
            color=(255, 255, 255),
            layer=1,
            collide=Rect(0, 0, 250, 60),
            color_on_hover=(200, 200, 200),
            color_on_mouse_down=(150, 150, 150),
            position=(
                (display_rect.w - 250) // 2,
                display_rect.h // 2 + 50
            )
        )
        
        button_text = nodeUI.TextUI(
            color=(0, 0, 0),
            layer=2,
            size=30,
            text='ПИКНУТЬ ИГРУ',
            filefont='./fonts/BoldPixels.ttf'
        )

        self.exit_button.append_children(button_text)
        
        button_text.position = Vector2D(
            (250 - button_text.collide.w) // 2,
            (60 - button_text.collide.h) // 2
        )
        self.exit_button.connect('_on_mouse_active', self._on_gameover, self)
        self.hide()
    
    def _on_gameover(self, button):
        systems.EventSystem()._running = False
        pass
    pass



class CounterDeathEnemy(nodeUI.NodeUI):

    name='CounterDeathEnemy'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.txt = nodeUI.TextUI(color=(0,0,0),
                      layer=10,
                      size=50,
                      text='0',
                      filefont='./fonts/BoldPixels.ttf'
                      )
                      
        self.txt.position += Vector2D(10, 10)
        
        self.append_children(self.txt)

        self.count = 0

        self.hide()
        pass

    def process(self, delta_time):

        l = systems.EventSystem().check_signal('kill_enemy')

        if l:
            self.count += len(l)
            self.txt.text = str(self.count)
            self.txt.update_shape()
        return super().process(delta_time)


    pass



