

class NodePool:
    def __init__(self, node_gen, capacity=16):

        self.pool = list()
        self.gen  = node_gen

        self.__genirate(capacity)
        pass

    def __genirate(self, count=16):
        for _ in range(count):
            ent = self.gen()
            self.pool.append(ent)
            ent.node_pool = self
            pass
        pass

    def acquire(self):

        if len(self.pool) == 0: self.__genirate()
        return self.pool.pop()
    
    def release(self, entity):
        if entity.node_pool is self:
            self.pool.append(entity)
        pass
    pass


class MultiEntityPool:
    def __init__(self):
        self.pools = dict()
        pass
    
    def register_type(self, obj_type, initial_size=16):
        self.pools[obj_type] = NodePool(obj_type, initial_size)
        pass
    
    def acquire(self, obj_type):
        pool = self.pools.get(obj_type)
        if pool:
            return pool.acquire()
        return None
    
    def release(self, obj):
        pool = self.pools.get(type(obj))
        if pool:
            pool.release(obj)
        pass