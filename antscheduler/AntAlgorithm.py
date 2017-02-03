
class MathOp:
    def __init__(self):
        pass

    MULTIPLY = 0
    ADD = 1


class AntAlgorithm:
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        self.config = _config
        self.nodes_list = _nodes_list
        self.ant_population = None
        self.result_history = []

    def graph_pheromone_clear(self):
        for node in self.nodes_list:
            node.pheromone_list = []

    def run(self):
        pass
