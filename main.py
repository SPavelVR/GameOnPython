
import pygame
import pygodot

import VSGamse

pygame.init()

pygodot.managers.Display((1200, 800), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)

pygodot.managers.ManagerFont().load('./fonts/BoldPixels.ttf', 30)
pygodot.systems.DrawSystem2D()
pygodot.systems.DrawSystemUI()
pygodot.systems.CollisionSystem()


node = pygodot.node2D.Node2D()

sc = pygodot.scenery.Scenery(root=node)

mainMenu = VSGamse.MainSelectionMenu()
node.append_children(mainMenu)

game = pygodot.node2D.Node2D(name='Game')
game.hide()
node.append_children(game)


deathMenu = VSGamse.DeathMenu()
node.append_children(deathMenu)
#node.append_children(VSGamse.PlayerNode())
#node.append_children(VSGamse.SpawnEnemiesNode())

#pygodot.node.print_all_tree(sc.root)

pygodot.timer.PyagemTimer()

while pygodot.systems.EventSystem()._running:
    pygodot.timer.PyagemTimer().update()
    delta = pygodot.timer.PyagemTimer().get_delta()
    pygodot.managers.Display().fill((255, 255, 255))

    sc.process(delta)

    pygodot.systems.CollisionSystem().process(delta)
    pygodot.systems.DrawSystem2D().process(delta)
    pygodot.systems.DrawSystemUI().process(delta)
    pygodot.systems.EventSystem().process(delta)

    
    pygodot.managers.Display().flip()
    pygame.time.delay(16)
    pass

pygodot.node.print_all_tree(sc.root)

sc.finaly()

pygodot.systems.DrawSystem2D().print_array()
pygodot.systems.DrawSystemUI().print_array()
print(pygodot.systems.EventSystem().node_array)
print(pygodot.systems.CollisionSystem().node_array)