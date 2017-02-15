import random
import logging

logger = logging.getLogger("AntScheduler.Ant")


class Ant:
    """Class representing one cycle of iteration and the result_permutation of this cycle"""

    def __init__(self, _start_node):
        self.visited_list = [_start_node]
        self.visibility_list = []
        self.result_value = None
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

    def next_node_calculate(self):
        pheromones_dict = self.visited_list[-1].get_pheromones(self.visibility_list)
        next_node = weighted_choice_sub(pheromones_dict)
        return next_node

    def result_generate(self):
        while self.visibility_list:
            next_node = self.next_node_calculate()
            self.ant_move(next_node)
        self.result_value = result_value_calculate_as_makespan(self.visited_list)


def weighted_choice_sub(_dict):
    rnd = random.random() * sum(_dict.values())
    for i, w in enumerate(_dict):
        rnd -= _dict[w]
        if rnd < 0:
            return w


def result_value_calculate_as_makespan(_operations):
    for i, operation in enumerate(_operations):
        machine_unload_time = get_machine_unload_time(_operations, i)
        if operation.predecessor_list:
            predecessor_end_times = [predecessor.start_time + predecessor.time_value for predecessor in
                                     operation.predecessor_list]
        else:
            predecessor_end_times = [0]
        operation.start_time = max([machine_unload_time] + predecessor_end_times)
    return _operations[-1].start_time + _operations[-1].time_value


def get_machine_unload_time(_operations, current):
    for i in reversed(range(current)):
        if _operations[i].type == _operations[current].type:
            return _operations[i].start_time + _operations[i].time_value
    return 0
