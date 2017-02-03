class GraphNode:
    """ Class representing nodes on process graph. It represents operation in industrial process"""

    def __init__(self, _name, _type, _time_value):
        self.name = _name
        self.type = _type
        self.time_value = _time_value
        self.successor_list = []
        self.pheromone_list = []
        self.predecessor_list = []

    def add_successor(self, _successor):
        self.successor_list.append(_successor)

    def add_predecessor(self, _predecessor):
        self.predecessor_list.append(_predecessor)

    def add_pheromone(self, _pheromone_edge):
        self.pheromone_list.append(_pheromone_edge)

    def get_pheromones(self, _nodes):
        pheromone_dict = {}
        for node in _nodes:
            pheromone_dict[node] = 1
            for pheromone in self.pheromone_list:
                if pheromone.successor in pheromone_dict:
                    pheromone_dict[pheromone.successor] = pheromone.value
        return pheromone_dict

    def return_nested_predecessors(self):
        nested_list = self.predecessor_list[:]
        if not nested_list:
            return []
        for node in nested_list:
            nested_list.extend(node.return_nested_predecessors())
        return nested_list
