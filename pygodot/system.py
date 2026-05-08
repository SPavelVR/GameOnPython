

class GameSystem:

    name_system: str    = None
    node_array: list    = None
    pause: bool         = False

    _instances = {}
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self, *args, **kw):
        if self._initialized: return None
        super().__init__(*args, **kw)

        self.node_array = list()
        self._initialized = True
        pass

    def add_node(self, node):
        if node is None or node.systems.get(self, None): return None
        self.node_array.append(node)
        node.systems[self]    = len(self.node_array) - 1
        pass

    def remove_node(self, node):
        if node is None or not (self in node.systems): return None

        self.node_array[node.systems[self]]                 = self.node_array[-1]
        self.node_array[-1].systems[self]                   = node.systems[self]
        self.node_array.pop()

        node.systems.pop(self)
        pass

    def clear(self):
        self.node_array.clear()

    def process(self, delta_time: int):
        pass

    def ready(self):
        pass

    def finaly(self):
        pass

    def __call__(self, delta_time):
        if self.pause: return False

        self.process(delta_time)
        pass
    pass
