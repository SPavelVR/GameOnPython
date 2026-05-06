
from .node import Node



class Scenery:

    root: Node = None

    def __init__(self, *args, **kw):
        self.root = kw.get("root", None)

        if self.root:
            self.root.include_tree(None, self)
        pass

    def append(self, node: Node):
        if self.root is None:
            self.root = node
            self.root.include_tree(None, self)
        else:
            self.root.append_children(node)
        pass

    def process(self, delta_time: int):
        if self.root is None: return
    
        self.root(delta_time)
        return
    
    def finaly(self):
        if self.root is None: return

        self.root._exit_tree()
    pass