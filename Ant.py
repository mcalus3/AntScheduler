import random
from Result import Result
import logging
logger = logging.getLogger("AntScheduler.Ant")


class Ant:
    """Class representing one cycle of iteration and the result of this cycle"""

    def __init__(self, _start_node):
        self.visited_list = [_start_node]
        self.visibility_list = []
        self.result = None
        self.visibility_list_update()

    def visibility_list_update(self):
        """to add a successor to visibility list you have to check if all it's predecessors are already visited"""
        for successor in self.visited_list[-1].successor_list:
            if set(successor.predecessor_list).issubset(self.visited_list):
                self.visibility_list.append(successor)

    def ant_move(self, _next_node):
        self.visited_list.append(_next_node)
        self.visibility_list.remove(_next_node)
        self.visibility_list_update()

    @staticmethod
    def weighted_choice(_pheromones_dict):
        choices = [(node, value) for node, value in _pheromones_dict.iteritems()]
        total = sum(w for c, w in choices)
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w
        logger.error("Shouldn't get here")
        return None

    def next_node_calculate(self):
        pheromones_dict = self.visited_list[-1].get_pheromones(self.visibility_list)
        next_node = self.weighted_choice(pheromones_dict)
        return next_node

    def result_generate(self):
        while self.visibility_list:
            next_node = self.next_node_calculate()
            self.ant_move(next_node)
        self.result = Result(self.visited_list)
