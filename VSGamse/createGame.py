


from pygodot import *
from .spawnEnemies import *



def CreateGame(root: node.Node):


    SpawnEnemiesNode(parent=root)

    cn = root.find_in_tree_node('CounterDeathEnemy')

    cn.show()

    pass


class BuilderGame(node2D.Node2D):


    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


        pass


    pass



class ControlScript(script.Script):


    def process(self, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F11]:
            managers.Display().set_mode((0, 0), pygame.FULLSCREEN)
        elif keys[pygame.K_F10]:
            managers.Display().set_mode((1200, 800), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
        return super().process(delta_time)

    pass