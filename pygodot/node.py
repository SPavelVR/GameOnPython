
from .variables import *

class Node:

    name: str = None            # Уникальное имя узла (базово ставиться тип ноды)
    type_name: str = "Node"

    parent = None
    children: list = None

    scene_tree = None

    systems: dict = None
    include_systems: list = None

    script = None

    signal: dict = None

    visible = True
    _pause   = False

    node_pool: list = None

    def __init__(self, *args, **kw):
        self.name = kw.get("name", self.name)
        if not self.name:
            self.name = self.type_name

        self.children = list()
        self.systems = dict()
        self.signal = dict()


        parent = kw.get("parent", None)

        if parent:
            parent.append_children(self)

        if "include_systems" in kw:
            self.include_systems = list(kw["include_systems"])
        pass

    def add_script(self, script):
        self.script = script
        self.script.owner = self
        pass

    def remove_script(self):
        if not self.script: return None
        self.script.owner = None
        self.script = None

    def connect(self, name_signal: str, func, node):
        pool = self.signal.get(name_signal)
        if pool is None:
            pool = list()
            self.signal[name_signal] = pool
            pass
        pool.append([node, func])

    def _call_signal(self, signal_name, *args, **kw):
        if self._pause or not self.visible: return None

        pool = self.signal.get(signal_name)
        if pool:
            for i in pool:
                if i[0] and not i[0].visible: continue
                i[1](*args, **kw)
        pass

    def append_children(self, *args):
        for i in args:
            if i.parent or i.scene_tree or i is self: continue

            self.children.append(i)
            i.child_index = len(self.children) - 1
            i.parent = self
            
            if self.scene_tree:
                i.include_tree(self, self.scene_tree)

            if self._pause:
                i.stop()

            if not self.visible:
                i.hide()

        pass

    def find_child(self, target, recursiv = True):
        if type(target) is int:
            return self.children[target]
        
        if type(target) is str:
            for child in self.children:
                if child.name == target: return child
            if recursiv:
                for child in self.children:
                    res = child.find_child(target, True)
                    if res: return res
            return None
        
        if not hasattr(target, 'child_index'): return None
        
        if not target.parent is self and recursiv:
            for i in self.children:
                res = i.find_child(target, True)
            return None
        elif not target.parent is self:
            return None
        return self.children[target.child_index]
    
    def find_children(self, name: str, type_name="", recursiv=True, res_list: list = None):
        if res_list is None:
            res_list = list()

        for i in range(len(self.children)):
            child = self.children[i]

            if child.name == name or child.type_name == type_name:
                res_list.append(child)
            
            pass
     
        if recursiv:
            for i in self.children:
                i.find_children(name, type_name, recursiv, res_list)
        return res_list
    
    def find_in_tree_node(self, name: str):
        if self.scene_tree is None: return None

        root = self.scene_tree.root

        if root.name == name: return root

        return root.find_child(name)
        

    def remove_child(self, target, recursiv = True):

        if type(target) is int:
            for i in range(target + 1, len(self.children)):
                self.children[i].child_index -= 1
            node = self.children.pop(target)
            node.parent = None
            node.child_index = -1
            node._exit_tree()
            return node
        
        if not hasattr(node, 'child_index'): return None
        
        if not node.parent is self and recursiv:
            for i in self.children:
                res = i.remove_child(target, True)
                if res: return res
            return None
        elif not node.parent is self: 
            return None
        
        for i in range(target.child_index + 1, len(self.children)):
            self.children[i].child_index -= 1
        node = self.children.pop(target.child_index)
        node.parent = None
        node.child_index = -1
        node._exit_tree()
        return node
    
    def quick_remove_child(self, target, recursiv = True):
        if type(target) is int:
            node = self.children[target]
            self.children[target] = self.children[-1]
            self.children[-1].child_index = target
            self.children.pop()
            node.parent = None
            node.child_index = -1
            node._exit_tree()
            return node

        if not hasattr(target, 'child_index'): return None
        
        node = self.children[target.child_index]
        self.children[target.child_index] = self.children[-1]
        self.children[target.child_index].child_index = target.child_index
        self.children.pop()
        node.parent = None
        node.child_index = -1
        node._exit_tree()
        return node


    
    def include_tree(self, node, tree)->bool:
        if self.scene_tree: return False

        self.scene_tree = tree

        if self.parent is None: self.parent = node

        for i in self.children:
            i.include_tree(node, tree)
            pass
        self.ready()
        return True

    def _exit_tree(self):
        for i in self.children:
            i._exit_tree()
        self.scene_tree = None
        self.finaly()
        pass

    def ready(self):
        if not self.scene_tree: return 

        self._call_signal("ready")
        if self.script: self.script.ready()

        if self.include_systems:
            for i in self.include_systems:
                i().add_node(self)
        pass

    def process(self, delta_time):
        pass

    def finaly(self):
        self._call_signal("finaly")
        for k in self.systems.copy().keys():
            k.remove_node(self)

        if self.node_pool:
            self.node_pool.release(self)
        pass

    def __str__(self):
        return f'<Node \'{self.type_name}\' name \'{self.name}\' id [{hex(id(self)).upper()[2:]}]  {self.visible}  {self._pause}>'
    
    def __repr__(self):
        return f'<Node {self.type_name} - {self.name}  {id(self)}>'

    def show(self):
        if self.parent and not self.parent.visible: return

        self.visible = True

        for i in self.children:
            i.show()
        pass

    def hide(self):
        self.visible = False

        for i in self.children:
            i.hide()
        pass

    def stop(self):
        if self._pause: return None

        self._pause = True

        for i in self.children:
            i.stop()
        pass

    def start(self):
        if not self._pause: return None

        self._pause = False

        for i in self.children:
            i.start()
        pass

    def __call__(self, delta_time):
        if not (self.scene_tree and self.visible and not self._pause): return None

        for c in self.children:
            c(delta_time)

        self.process(delta_time)
        if self.script: self.script(delta_time)
        pass


    pass


def print_all_tree(root: Node, count_tabs = 0):

    if count_tabs: print('-' * count_tabs, end='')
    print(root)

    for c in root.children:
        print_all_tree(c, count_tabs + 1)
    pass